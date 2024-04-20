package handlers

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) CreateOrder(w http.ResponseWriter, r *http.Request) {

	// Take user claims
	ctx := r.Context()
	claims, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	// Receive order
	var order models.Order
	err := json.NewDecoder(r.Body).Decode(&order)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	order.ID = 0
	// Get cart
	err = h.DB.Preload("Goods").Find(&order.Cart, models.Cart{Model: models.Model{ID: order.CartID}, IsActive: true}).Error
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Check user
	if order.Cart.UserID != claims.ID {
		fmt.Println(order.Cart.UserID, claims.ID)
		utils.ResponseWithError(w, r, errors.New("wrong user"), http.StatusBadRequest)
	}

	// Make current cart inactive
	order.Cart.IsActive = false
	saveResult := h.DB.Save(&order.Cart)
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}

	//Create new cart
	saveResult = h.DB.Create(&models.Cart{UserID: claims.ID, IsActive: true})
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}

	// check if all merch still available
	for _, m := range order.Cart.Goods {
		if m.Status != "available" {
			utils.ResponseWithError(w, r, errors.New("merchandise already sold"), http.StatusBadRequest)
		}
	}

	// change merch status to ordered
	for _, m := range order.Cart.Goods {
		m.Status = "ordered"
		saveResult = h.DB.Save(&m)
		if saveResult.Error != nil {
			utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
		}
	}

	//Create order
	order.UserID = claims.ID
	saveResult = h.DB.Create(&order)
	order.Cart = nil
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(order)
}
