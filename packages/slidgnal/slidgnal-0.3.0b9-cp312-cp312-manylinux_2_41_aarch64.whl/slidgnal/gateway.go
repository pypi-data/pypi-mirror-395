package signal

import (
	// Standard library.
	"context"
	"os"
	"runtime"

	// Third-party libraries.
	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
	"github.com/rs/zerolog"
	"go.mau.fi/mautrix-signal/pkg/signalmeow/store"
	"go.mau.fi/util/dbutil"
)

const (
	// Maximum number of concurrent gateway calls to handle before blocking.
	maxConcurrentGatewayCalls = 1024
)

// A LinkedDevice represents a unique pairing session between the gateway and Signal. It is not
// unique to the underlying "main" device (or user/phone number), as multiple linked devices may be
// paired with any main device.
type LinkedDevice struct {
	// ID is an opaque string identifying this [LinkedDevice] to a [Session]. Noted that this string
	// is currently equivalent to a password, and needs to be protected accordingly.
	ID string

	// Whether or not we've previously tried to sync this device from the main device's archive.
	ArchiveSynced bool
}

// CastUUID receives a byte slice and returns a valid [uuid.UUID] if the slice is exactly 16 bytes,
// or [uuid.Nil] otherwise.
func castUUID(b []byte) uuid.UUID {
	if len(b) == 16 {
		return uuid.UUID(b)
	}
	return uuid.Nil
}

type Gateway struct {
	// Common configuration.
	DBPath   string
	Name     string
	LogLevel string

	// Internal fields.
	callChan chan (func())
	store    *store.Container
	log      zerolog.Logger
}

func NewGateway() *Gateway {
	return &Gateway{}
}

func (w *Gateway) Init() error {
	var ctx = context.Background()

	// Set up logging.
	w.log = zerolog.New(os.Stdout).Level(logLevel(w.LogLevel))

	// Initialize database connection.
	db, err := dbutil.NewWithDialect("file:"+w.DBPath, "sqlite3")
	if err != nil {
		return err
	}

	// Initialize device store.
	w.store = store.NewStore(db, dbutil.ZeroLogger(w.log))
	if err = w.store.Upgrade(ctx); err != nil {
		return err
	}

	w.callChan = make(chan func(), maxConcurrentGatewayCalls)
	go func() {
		// Don't allow other Goroutines from using this thread, as this might lead to concurrent use of
		// the GIL, which can lead to crashes.
		runtime.LockOSThread()
		defer runtime.UnlockOSThread()
		for fn := range w.callChan {
			fn()
		}
	}()

	return nil
}

// LogLevel returns a concrete [zerolog.Level] for the Python logging level string given.
func logLevel(l string) zerolog.Level {
	switch l {
	case "FATAL", "CRITICAL":
		return zerolog.FatalLevel
	case "ERROR":
		return zerolog.ErrorLevel
	case "WARN", "WARNING":
		return zerolog.WarnLevel
	case "DEBUG":
		return zerolog.DebugLevel
	default:
		return zerolog.InfoLevel
	}
}
