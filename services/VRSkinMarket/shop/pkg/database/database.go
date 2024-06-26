package database

import (
	"template/gateway/pkg/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Database struct {
	DB *gorm.DB
}

func CreateDatabase(connectionURL string) (*gorm.DB, error) {
	db, err := gorm.Open(
		postgres.Open(connectionURL),
		&gorm.Config{},
	)
	if err != nil {
		return db, err
	}
	if err := db.AutoMigrate(&models.User{}); err != nil {
		return db, err
	}
	if err := db.AutoMigrate(&models.Cart{}); err != nil {
		return db, err
	}
	if err := db.AutoMigrate(&models.Order{}); err != nil {
		return db, err
	}
	if err := db.AutoMigrate(&models.Merchandise{}); err != nil {
		return db, err
	}
	return db, nil
}
