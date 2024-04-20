package handlers

import (
	"net/http"
	"time"
)

func (h Handler) Logout(w http.ResponseWriter, r *http.Request) {
	// Set a cookie
	http.SetCookie(w, &http.Cookie{
		Name:    "token",
		Value:   "",
		Expires: time.Now(),
	})
	// Send a 200 ok response
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
