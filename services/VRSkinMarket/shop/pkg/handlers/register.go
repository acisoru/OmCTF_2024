package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) Register(w http.ResponseWriter, r *http.Request) {
	// Decode user input
	var user models.User
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Default user role is... well.. user!
	user.Role = "user"

	// Check that there is no other user with that username
	var count int64
	resultSearch := h.DB.Model(&models.User{}).Where("username = ?", user.Username).Count(&count)
	if resultSearch.Error != nil {
		utils.ResponseWithError(w, r, resultSearch.Error, http.StatusBadRequest)
	}
	if count > 0 {
		utils.ResponseWithError(w, r, errors.New("user with that username already exists"), http.StatusBadRequest)
	}

	// Create a hash
	user.Password, err = utils.HashPassword(user.Password)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Append to the Users table
	user.Carts = append(user.Carts, models.Cart{UserID: user.ID, IsActive: true})
	result := h.DB.Create(&user)
	if result.Error != nil {
		utils.ResponseWithError(w, r, result.Error, http.StatusBadRequest)
	}

	//Create new cart
	saveResult := h.DB.Save(&user)
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}

	// Send a 201 created response
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}
