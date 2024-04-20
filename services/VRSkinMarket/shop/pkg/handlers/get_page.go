package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"template/gateway/pkg/models"
	"template/gateway/pkg/utils"
)

func (h Handler) GetPage(w http.ResponseWriter, r *http.Request) {

	// Take user claims
	ctx := r.Context()

	_, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	// Receive pagination
	var pagination models.Pagination
	err := json.NewDecoder(r.Body).Decode(&pagination)
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	var merch []models.Merchandise
	h.DB.Scopes(models.Paginate(merch, &pagination, h.DB)).Find(&merch, models.Merchandise{Status: "available"})
	for i, _ := range merch {
		merch[i].NFTToken = "Buy to see!"
	}
	pagination.Rows = merch
	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	err = json.NewEncoder(w).Encode(pagination)
	if err != nil {
		if !ok {
			utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
		}
	}
}
