package main

import (
	"log"
	"net/http"
	"template/gateway/pkg/config"
	"template/gateway/pkg/database"
	"template/gateway/pkg/handlers"
	"template/gateway/pkg/middlewares"

	"github.com/gorilla/mux"
)

func main() {
	log.Println("Reading config")
	conf, err := config.CreateConfig()
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Init DB")
	DB, err := database.CreateDatabase(conf.DBAddr)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Init middlewares")
	m, err := middlewares.CreateMiddleware(conf.JWTKey)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Init handlers")
	h, err := handlers.CreateHandler(DB, conf.TokenExpirationTime, conf.JWTKey)
	if err != nil {
		log.Fatal(err)
	}
	router := mux.NewRouter()
	router.Use(m.PanicRecovery, m.Logging, m.Authenticated)
	router.HandleFunc("/api/v1/health", h.Health).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/register", h.Register).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/invite", h.InviteRegister).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/login", h.Login).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/refresh", h.Refresh).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/logout", h.Logout).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/change-password", h.ChangePassword).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/profile", h.GetProfile).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/profile", h.UpdateProfile).Methods(http.MethodPut)
	router.HandleFunc("/api/v1/order", h.GetOrder).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/order", h.CreateOrder).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/cart", h.GetCart).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/cart", h.UpdateCart).Methods(http.MethodPut)
	router.HandleFunc("/api/v1/cart", h.DeleteFromCart).Methods(http.MethodDelete)
	router.HandleFunc("/api/v1/merchandise", h.GetMerch).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/my_merchandise", h.AddMerch).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/my_merchandise", h.GetMyMerch).Methods(http.MethodGet)
	router.HandleFunc("/api/v1/buy", h.Buy).Methods(http.MethodPost)
	router.HandleFunc("/api/v1/catalogue", h.GetPage).Methods(http.MethodPost)
	http.Handle("/", router)
	server := &http.Server{
		Handler: router,
		Addr:    conf.BindAddr,
	}
	log.Printf("Starting server on %v with db connection to %v", conf.BindAddr, conf.DBAddr)
	log.Println(server.ListenAndServe())
}
