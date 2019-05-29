package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func main() {
	resp, _ := http.Get("http://icanhazwordz.appspot.com/dictionary.words")
	body, _ := ioutil.ReadAll(resp.Body)  // This fails on play.golang.org because it's sandboxed, but will work if run locally.
	words := strings.Split(string(body), "\n")
	fmt.Println(words[:10])
	fmt.Println(len(words))
}

