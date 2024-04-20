package models

type User struct {
	Model
	Username  string        `gorm:"unique" json:"username"`
	Password  string        `json:"password"`
	Role      string        `json:"role"`
	Cash      int64         `json:"cash"`
	Flag      string        `json:"flag"`
	AvatarURL string        `json:"avatar_url"`
	Status    string        `json:"status"`
	Carts     []Cart        `gorm:"foreignKey:UserID" json:"carts"`
	Merch     []Merchandise `gorm:"foreignKey:UserID" json:"merchandise"`
	Orders    []Order       `gorm:"foreignKey:UserID" json:"orders"`
}
