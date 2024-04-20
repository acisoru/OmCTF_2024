package middlewares

import (
	"context"
	"errors"
	"net/http"
	"template/gateway/pkg/utils"
)

func (m Middleware) Authenticated(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
		c, err := req.Cookie("token")
		if err != nil {
			if errors.Is(err, http.ErrNoCookie) {
				next.ServeHTTP(w, req)
				return
			}
			utils.ResponseWithError(w, req, err, http.StatusInternalServerError)
		}
		claims, err := utils.ParseToken(c.Value, m.JWTKey)
		if err != nil {
			utils.ResponseWithError(w, req, err, http.StatusInternalServerError)
		}
		ctx := req.Context()
		ctx = context.WithValue(ctx, "claims", claims)
		next.ServeHTTP(w, req.WithContext(ctx))
	})

}
