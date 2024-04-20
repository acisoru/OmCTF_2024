package handlers

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) GetProfile(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()
	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}
	// Get a user
	var user models.User
	fmt.Println(claims.ID)
	queryResult := h.DB.Find(&user, models.User{Model: models.Model{ID: claims.ID}})
	user.Password = ""
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusNotFound)
	}
	queryResult = h.DB.Find(&user.Orders, models.Order{UserID: claims.ID})
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusInternalServerError)
	}
	queryResult = h.DB.Find(&user.Merch, models.Merchandise{UserID: claims.ID})
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusInternalServerError)
	}
	//queryResult := h.DB.Model(models.User{Model: gorm.Model{ID: claims.ID}})

	// Send a 201 created response
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	err := json.NewEncoder(w).Encode(user)
	if err != nil {
		if !ok {
			utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
		}
	}
}
