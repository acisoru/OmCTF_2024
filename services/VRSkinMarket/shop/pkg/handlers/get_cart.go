package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) GetCart(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()
	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	// Get active cart for current user
	var cart models.Cart
	err := h.DB.Preload("Goods").Find(&cart, models.Cart{UserID: claims.ID, IsActive: true}).Error
	//queryResult := h.DB.Where(&models.Cart{UserID: claims.ID, IsActive: true}).First(&cart)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	for i, _ := range cart.Goods {
		cart.Goods[i].NFTToken = "Buy to see!"
	}
	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	err = json.NewEncoder(w).Encode(cart)
	if err != nil {
		if !ok {
			utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
		}
	}
}
