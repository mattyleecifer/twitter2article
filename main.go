package main

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"strings"
	"text/template"
	"time"
)

type sitevars struct {
	Success bool
	Ans     string
	Opt1    string
	Opt2    string
	Opt3    string
	Opt4    string
}

type input struct {
	text  string
	Input string
	Ans   string
}

func main() {
	// http.HandleFunc("/", mainPage)
	http.HandleFunc("/", convert)
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func convert(w http.ResponseWriter, r *http.Request) {
	s := sitevars{}

	tmpl := template.Must(template.ParseFiles("main.html"))
	if r.Method != http.MethodPost {
		tmpl.Execute(w, s)
		return
	}

	i := input{
		Input: r.FormValue("input"),
	}

	fmt.Println(i.Input)

	output := pylaunch(i.Input)
	output = strings.TrimPrefix(output, "b'")
	output = strings.TrimSuffix(output, "<p>'") // not really working but not a priority
	fmt.Println(output)
	s.Ans = output
	s.Opt1 = i.Input
	tmpl.Execute(w, s)
}

func pylaunch(s string) string {
	c1 := make(chan string, 1)

	// Returning text through channel allows us to create timeout
	go func() {
		text, _ := exec.Command("py", "twitter2article.py", s).Output()
		//text, _ := exec.Command("py", "test.py", s).Output()
		// ok so the test python file works
		c1 <- string(text)
	}()

	// Listen on our channel AND a timeout channel - which ever happens first.
	select {
	case res := <-c1:
		fmt.Println(res)
		return res
	case <-time.After(120 * time.Second):
		fmt.Println("out of time :(")
		return "Timed out"
	}

}
