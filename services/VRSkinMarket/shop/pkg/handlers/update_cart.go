package handlers

import (
	"errors"
	"fmt"
	"gorm.io/gorm"
	"net/http"
	"strconv"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) UpdateCart(w http.ResponseWriter, r *http.Request) {
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
	//var merch models.Merchandise
	//err := json.NewDecoder(r.Body).Decode(&merch)
	//if err != nil {
	//	utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	//}

	// Get cart
	var cart models.Cart
	getResult := h.DB.Preload("Goods").Find(&cart, models.Cart{UserID: claims.ID, IsActive: true})
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

	// Check merch status
	if DBmerch.Status != "available" {
		utils.ResponseWithError(w, r, errors.New("already sold or reserved"), http.StatusBadRequest)
	}

	// Add merch to cart
	for _, m := range cart.Goods {
		if m.ID == DBmerch.ID {
			utils.ResponseWithError(w, r, errors.New("already in cart"), http.StatusBadRequest)
		}
	}
	cart.Goods = append(cart.Goods, DBmerch)
	cart.TotalQuantity += 1
	cart.TotalPrice += DBmerch.Price
	// Save cart
	saveResult := h.DB.Session(&gorm.Session{FullSaveAssociations: true}).Updates(&cart)
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}

	// Update cart
	h.DB.Save(&cart)
	//h.DB.Model(&models.Cart{UserID: claims.ID, IsActive: true}).Updates(&models.Cart{Goods: cart.Goods, TotalQuantity: cart.TotalQuantity, TotalPrice: cart.TotalPrice})

	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
