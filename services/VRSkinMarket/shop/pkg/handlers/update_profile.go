package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) UpdateProfile(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()
	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}
	// Decode only changeable fields
	var fields models.UpdatableUserFields
	err := json.NewDecoder(r.Body).Decode(&fields)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	var user models.User
	queryResult := h.DB.Where(&models.User{Model: models.Model{ID: claims.ID}}).First(&user)
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusNotFound)
	}
	// Func will be cleaner, DRY
	CheckAndChange := func(a, b *string) {
		if len(*a) > 0 {
			*b = *a
		}
	}
	CheckAndChange(&fields.AvatarURL, &user.AvatarURL)
	// Saving and returning resulted updated user
	updateResult := h.DB.Save(&user)
	if updateResult.Error != nil {
		utils.ResponseWithError(w, r, updateResult.Error, http.StatusBadRequest)
	}
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(&user)
}
