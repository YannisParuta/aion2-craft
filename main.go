// AION 2 — Calculateur de craft
// Petit exécutable autonome : sert l'interface en local (127.0.0.1) et l'ouvre
// dans une fenêtre Microsoft Edge en mode application (sinon dans le navigateur par défaut).
// Les réglages (stock, prix, niveau…) sont enregistrés dans %APPDATA%\AionCraftCalc\state.json.
package main

import (
	"embed"
	"io"
	"io/fs"
	"log"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sync"
	"time"
)

//go:embed web/* data.json
var assets embed.FS

var (
	mu       sync.Mutex
	lastPing = time.Now()
	byeAt    time.Time
)

func appDir() string {
	base := os.Getenv("APPDATA")
	if base == "" {
		base, _ = os.UserConfigDir()
	}
	if base == "" {
		base = "."
	}
	d := filepath.Join(base, "AionCraftCalc")
	os.MkdirAll(d, 0o755)
	return d
}

func main() {
	dir := appDir()
	logf, err := os.OpenFile(filepath.Join(dir, "app.log"), os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0o644)
	if err == nil {
		log.SetOutput(logf)
	}
	statePath := filepath.Join(dir, "state.json")

	web, _ := fs.Sub(assets, "web")
	mux := http.NewServeMux()
	mux.Handle("/", http.FileServer(http.FS(web)))
	mux.HandleFunc("/data.json", func(w http.ResponseWriter, r *http.Request) {
		b, _ := assets.ReadFile("data.json")
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		w.Write(b)
	})
	mux.HandleFunc("/api/state", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			b, err := os.ReadFile(statePath)
			if err != nil {
				http.Error(w, "no state", http.StatusNotFound)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.Write(b)
		case http.MethodPost:
			b, err := io.ReadAll(io.LimitReader(r.Body, 2<<20))
			if err != nil {
				http.Error(w, err.Error(), 400)
				return
			}
			tmp := statePath + ".tmp"
			if err := os.WriteFile(tmp, b, 0o644); err == nil {
				os.Rename(tmp, statePath)
			}
			w.WriteHeader(204)
		}
	})
	mux.HandleFunc("/api/ping", func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		lastPing = time.Now()
		byeAt = time.Time{}
		mu.Unlock()
		w.WriteHeader(204)
	})
	mux.HandleFunc("/api/bye", func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		byeAt = time.Now()
		mu.Unlock()
		w.WriteHeader(204)
	})

	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		log.Fatal(err)
	}
	url := "http://" + ln.Addr().String() + "/"
	log.Println("serveur sur", url)
	go http.Serve(ln, mux)

	if os.Getenv("AIONCRAFT_NOBROWSER") == "" {
		openWindow(url, dir)
	}

	// Arrêt : fenêtre fermée (signal "bye" non suivi d'un ping) ou plus aucun ping depuis 3 min.
	for {
		time.Sleep(1 * time.Second)
		mu.Lock()
		quit := (!byeAt.IsZero() && time.Since(byeAt) > 4*time.Second) || time.Since(lastPing) > 3*time.Minute
		mu.Unlock()
		if quit {
			log.Println("fermeture")
			return
		}
	}
}

func openWindow(url, dir string) {
	if runtime.GOOS != "windows" {
		exec.Command("xdg-open", url).Start()
		return
	}
	candidates := []string{
		filepath.Join(os.Getenv("ProgramFiles(x86)"), `Microsoft\Edge\Application\msedge.exe`),
		filepath.Join(os.Getenv("ProgramFiles"), `Microsoft\Edge\Application\msedge.exe`),
		filepath.Join(os.Getenv("LOCALAPPDATA"), `Microsoft\Edge\Application\msedge.exe`),
		filepath.Join(os.Getenv("ProgramFiles"), `Google\Chrome\Application\chrome.exe`),
		filepath.Join(os.Getenv("ProgramFiles(x86)"), `Google\Chrome\Application\chrome.exe`),
		filepath.Join(os.Getenv("LOCALAPPDATA"), `Google\Chrome\Application\chrome.exe`),
	}
	profile := filepath.Join(dir, "fenetre")
	for _, p := range candidates {
		if _, err := os.Stat(p); err == nil {
			cmd := exec.Command(p, "--app="+url, "--user-data-dir="+profile,
				"--window-size=1400,900", "--no-first-run", "--no-default-browser-check")
			if err := cmd.Start(); err == nil {
				log.Println("fenêtre ouverte avec", p)
				return
			}
		}
	}
	// repli : navigateur par défaut
	exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
}
