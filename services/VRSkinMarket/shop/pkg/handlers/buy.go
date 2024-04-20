package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) Buy(w http.ResponseWriter, r *http.Request) {

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
	if order.Cart == nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Get user
	var user models.User
	queryResult := h.DB.Find(&user, models.User{Model: models.Model{ID: claims.ID}})
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusBadRequest)
	}

	// Check balance
	if user.Cash < order.Cart.TotalPrice {
		utils.ResponseWithError(w, r, errors.New("not enough DogeCoins"), http.StatusBadRequest)
	}

	// Get order
	err = h.DB.Find(&order, models.Order{Model: models.Model{ID: order.ID}}).Error
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	// Get cart
	err = h.DB.Preload("Goods").Find(&order.Cart, models.Cart{Model: models.Model{ID: order.CartID}}).Error
	//getResult := h.DB.Find(&order.Cart, models.Cart{Model: models.Model{ID: order.Cart.ID}})
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}

	// Check user
	if order.Cart.UserID != claims.ID {
		utils.ResponseWithError(w, r, errors.New("wrong user"), http.StatusBadRequest)
	}
	if order.UserID != claims.ID {
		utils.ResponseWithError(w, r, errors.New("wrong user"), http.StatusBadRequest)
	}

	// Update user cash
	user.Cash -= order.Cart.TotalPrice
	saveResult := h.DB.Model(&models.User{}).Where("ID = ?", user.ID).Update("cash", user.Cash)
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}
	//// Get merch
	//getResult := h.DB.Find(&order.Cart.Goods, models.Merchandise{CartID: order.Cart.ID})
	//if getResult.Error != nil {
	//	utils.ResponseWithError(w, r, getResult.Error, http.StatusBadRequest)
	//}

	// give money and transfer merch
	for _, m := range order.Cart.Goods {
		var user models.User
		queryResult := h.DB.Find(&user, models.User{Model: models.Model{ID: m.UserID}})
		if queryResult.Error != nil {
			utils.ResponseWithError(w, r, queryResult.Error, http.StatusInternalServerError)
		}
		user.Cash += m.Price
		m.UserID = claims.ID
		m.Status = "bought"
		saveResult := h.DB.Model(&models.User{}).Where("ID = ?", user.ID).Update("cash", user.Cash)
		if saveResult.Error != nil {
			utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
		}
		saveResult = h.DB.Save(&m)
		if saveResult.Error != nil {
			utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
		}
	}

	// Update order status
	order.Status = "paid"
	saveResult = h.DB.Save(&order)
	if saveResult.Error != nil {
		utils.ResponseWithError(w, r, saveResult.Error, http.StatusInternalServerError)
	}

	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
