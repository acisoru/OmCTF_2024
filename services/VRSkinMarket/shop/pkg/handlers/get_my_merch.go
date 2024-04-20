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

func (h Handler) GetMyMerch(w http.ResponseWriter, r *http.Request) {
	// Take user claims
	ctx := r.Context()

	_, ok := ctx.Value("claims").(*models.Claims)
	if !ok {
		utils.ResponseWithError(w, r, errors.New("no cookie"), http.StatusUnauthorized)
	}

	var merch models.Merchandise
	id, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		utils.ResponseWithError(w, r, err, http.StatusBadRequest)
	}
	queryResult := h.DB.Where(fmt.Sprintf("ID = %v", id)).First(&merch)
	if queryResult.Error != nil {
		utils.ResponseWithError(w, r, queryResult.Error, http.StatusBadRequest)
	}

	// Response with status ok!
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	err = json.NewEncoder(w).Encode(merch)
	if err != nil {
		if !ok {
			utils.ResponseWithError(w, r, err, http.StatusInternalServerError)
		}
	}
}
