package utils

import (
	"fmt"
	"template/gateway/pkg/models"

	"github.com/golang-jwt/jwt"
)

func ParseToken(tokenString string, key string) (claims *models.Claims, err error) {
	token, err := jwt.ParseWithClaims(tokenString, &models.Claims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(key), nil
	})
	if err != nil {
		return &models.Claims{}, err
	}
	if claims, ok := token.Claims.(*models.Claims); ok {
		fmt.Println(claims.ID)
		return claims, nil

	}
	fmt.Println(claims)
	return &models.Claims{}, err
}
