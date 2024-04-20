package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) ChangePassword(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()
	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	// Receive inputted password
	var creds models.Credentials
	err := json.NewDecoder(r.Body).Decode(&creds)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Create hashed password
	password, err := utils.HashPassword(creds.Password)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Update password hash in database
	updateResult := h.DB.Model(&models.User{Model: models.Model{ID: claims.ID}}).Update("password", password)
	if updateResult.Error != nil {
		utils.ResponseWithError(w, r, updateResult.Error, http.StatusBadRequest)
	}

	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
