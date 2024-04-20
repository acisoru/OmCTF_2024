package handlers

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strconv"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) GetOrder(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()

	//Prolly should do something with this shite
	_, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	var order models.Order
	id, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	//TODO here
	queryResult := h.DB.First(&order, fmt.Sprintf("ID = %v", id))
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusBadRequest)
	}
	queryResult = h.DB.Preload("Goods").Find(&order.Cart, fmt.Sprintf("ID = %v", order.CartID))
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusBadRequest)
	}
	if order.Status != "paid" {
		for i, _ := range order.Cart.Goods {
			order.Cart.Goods[i].NFTToken = "Buy to see!"
		}
	}
	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	err = json.NewEncoder(w).Encode(order)
	if err != nil {
		if !ok {
			utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
		}
	}
}
