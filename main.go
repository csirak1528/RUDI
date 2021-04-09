package main

import (
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"github.com/gorilla/mux"
)

func authUser(w http.ResponseWriter, router *http.Request) {

}
func getFile(w http.ResponseWriter, router *http.Request) {

}
func distribute(w http.ResponseWriter, router *http.Request) {

}
func deleteFile(w http.ResponseWriter, router *http.Request) {

}
func updateFile(w http.ResponseWriter, router *http.Request) {

}

func main() {
	router := mux.NewRouter()

	router.HandleFunc("/api/user/auth", authUser).Methods("PUT")
	router.HandleFunc("/api/file/{name}", getFile).Methods("GET")
	router.HandleFunc("/api/file/distribute/{name}", distribute).Methods("PUT")
	router.HandleFunc("/api/file/{name}", deleteFile).Methods("DELETE")
	router.HandleFunc("/api/file/{name}", updateFile).Methods("PUT")

	log.Fatal(http.ListenAndServe(":8000", router))
}