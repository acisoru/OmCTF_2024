package models

import (
	"gorm.io/gorm"
	"time"
)

type Model struct {
	ID        uint `gorm:"index"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt
}
