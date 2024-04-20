package handlers

import (
	"errors"
	"fmt"
	"net/http"
	"strconv"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) DeleteFromCart(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()
	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	// Receive merch
	id, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Get cart
	var cart models.Cart
	getResult := h.DB.Find(&cart, models.Cart{UserID: claims.ID, IsActive: true})
	if getResult.Error != nil {
		utils.ResponseWithError(w, r, getResult.Error, http.StatusBadRequest)
	}

	// Check user
	if cart.UserID != claims.ID {
		utils.ResponseWithError(w, r, errors.New("wrong user"), http.StatusBadRequest)
	}

	// Get merch
	var DBmerch models.Merchandise
	getResult = h.DB.Find(&DBmerch, fmt.Sprintf("ID = %v", id))
	if getResult.Error != nil {
		utils.ResponseWithError(w, r, getResult.Error, http.StatusBadRequest)
	}
	cart.TotalQuantity -= 1
	cart.TotalPrice -= DBmerch.Price
	err = h.DB.Model(&cart).Association("Goods").Delete(DBmerch)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
	}
	// Update cart
	h.DB.Save(&cart)

	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
