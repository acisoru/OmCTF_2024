package handlers

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) AddMerch(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()

	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	// Receive merch
	var merch models.Merchandise
	err := json.NewDecoder(r.Body).Decode(&merch)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	merch.UserID = claims.ID
	merch.Status = "available"

	var user models.User
	fmt.Println(claims.ID)
	err = h.DB.Model(&models.User{}).Where(models.User{Model: models.Model{ID: claims.ID}}).Select("username").Find(&user).Error
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	merch.Seller = user.Username
	createStatus := h.DB.Create(&merch)
	if createStatus.Error != nil {
		utils.ResponseWithError(w, r, createStatus.Error, http.StatusInternalServerError)
	}
	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	err = json.NewEncoder(w).Encode(merch)
	if err != nil {
		if !ok {
			utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
		}
	}
}
