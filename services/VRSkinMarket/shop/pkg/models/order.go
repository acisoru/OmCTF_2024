package models

type Order struct {
	Model
	UserID uint   `json:"user_id"`
	CartID uint   `json:"cart_id"`
	Cart   *Cart  `json:"cart"`
	Status string `json:"status"`
}
