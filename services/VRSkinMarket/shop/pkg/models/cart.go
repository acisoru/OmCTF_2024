package models

type Cart struct {
	Model
	//OrderID       uint           `json:"order_id"`
	UserID        uint          `gorm:"foreignKey:ID" json:"user_id"`
	Goods         []Merchandise `gorm:"many2many:goods;" json:"goods"`
	TotalQuantity uint          `json:"total_quantity"`
	TotalPrice    int64         `json:"price"`
	IsActive      bool          `json:"is_active"`
}
