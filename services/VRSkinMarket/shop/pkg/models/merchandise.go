package models

type Merchandise struct {
	Model
	UserID      uint   `gorm:"foreignKey:ID" json:"user_id"`
	Seller      string `json:"seller"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Price       int64  `json:"price"`
	Picture     string `json:"picture"`
	NFTToken    string `json:"NFTToken"`
	Status      string `json:"status"`
}
