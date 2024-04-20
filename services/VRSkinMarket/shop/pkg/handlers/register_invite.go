package handlers

import (
	"encoding/json"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) InviteRegister(w http.ResponseWriter, r *http.Request) {
	// Decode user input
	var user models.User
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Default user role is... well.. user!
	user.Role = "user"

	//TODO check who invited and give bonus

	// Create a hash
	user.Password, err = utils.HashPassword(user.Password)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Append to the Users table
	result := h.DB.Save(&user)
	if result.Error != nil {
		utils.ResponseWithError(w, r, result.Error, http.StatusBadRequest)
	}

	// Send a 201 created response
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}
