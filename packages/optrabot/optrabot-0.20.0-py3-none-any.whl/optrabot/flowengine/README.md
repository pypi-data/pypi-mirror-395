# FlowEngine - OptraBot Automation Engine

Die FlowEngine ermöglicht die Automatisierung von Aktionen basierend auf Trading-Events.

## Überblick

Die FlowEngine besteht aus folgenden Komponenten:

- **FlowEngine**: Singleton-Klasse, die Flows verwaltet und Events verarbeitet
- **Flow**: Konfiguration eines Flows mit Event-Trigger und Actions
- **FlowEvent**: Event-Datenstrukturen für verschiedene Trading-Events
- **Actions**: Ausführbare Aktionen wie Notifications oder Template-Processing

## Event-Typen

### 1. `trade_opened`
Wird ausgelöst, wenn ein Trade erfolgreich eröffnet wurde.

**Verfügbare Variablen:**
- `$EVENT_TRADE_ID`: Trade-ID
- `$EVENT_TRADE_AMOUNT`: Anzahl der Kontrakte
- `$EVENT_TRADE_ENTRY_PRICE`: Einstiegspreis
- `$EVENT_TRADE_SYMBOL`: Handelssymbol (z.B. SPX)
- `$EVENT_TRADE_STRATEGY`: Strategie-Name
- `$EVENT_TRADE_EXPIRATION`: Verfallsdatum der Optionen (datetime.date)

### 2. `early_exit`
Wird ausgelöst, wenn ein Trade vorzeitig geschlossen wird (z.B. bei Breakeven).

**Verfügbare Variablen:**
- `$EVENT_TRADE_ID`: Trade-ID
- `$EVENT_TRADE_AMOUNT`: Anzahl der Kontrakte
- `$EVENT_TRADE_ENTRY_PRICE`: Einstiegspreis
- `$EVENT_TRADE_EXIT_PRICE`: Ausstiegspreis
- `$EVENT_TRADE_NET_RESULT`: Netto-Ergebnis des Trades (Gewinn/Verlust nach Abzug aller Fees)
- `$EVENT_TRADE_PREMIUM`: Erhaltene/Gezahlte Prämie bei Eröffnung
- `$EVENT_TRADE_FEES`: Summe aller Fees und Commissions des Trades
- `$EVENT_TRADE_SYMBOL`: Handelssymbol
- `$EVENT_TRADE_STRATEGY`: Strategie-Name
- `$EVENT_TRADE_EXPIRATION`: Verfallsdatum der Optionen (datetime.date)

### 3. `stop_loss_hit`
Wird ausgelöst, wenn die Stop-Loss-Order ausgeführt wurde.

**Verfügbare Variablen:** Gleiche wie bei `early_exit`

### 4. `take_profit_hit`
Wird ausgelöst, wenn die Take-Profit-Order ausgeführt wurde.

**Verfügbare Variablen:** Gleiche wie bei `early_exit`

## Actions

### 1. `send_notification`
Sendet eine Notification über den TradingHub.

**Parameter:**
- `message`: Nachrichtentext (kann Variablen enthalten)
- `type`: Notification-Typ (`INFO`, `WARN`, `ERROR`) - Optional, Standard: `INFO`

**Beispiel:**
```yaml
- send_notification:
    message: "Trade $EVENT_TRADE_ID wurde geschlossen. Ergebnis: $$EVENT_TRADE_NET_RESULT"
    type: INFO
```

### 2. `process_template`
Verarbeitet ein Trade-Template mit konfigurierten oder berechneten Parametern.

**Parameter:**
- `template`: Name des zu verarbeitenden Templates
- `amount`: Anzahl der Kontrakte (statisch oder als Formel)
- `premium`: Erwartete Prämie (statisch oder als Formel)
- `expiration`: Optionales Verfallsdatum (statisch als datetime.date oder als Formel, z.B. `$EVENT_TRADE_EXPIRATION`)
- `time`: Optionale Zeitangabe für verzögerte Ausführung (Format: "HH:MM <Timezone>", z.B. "15:00 EST")

**Beispiel:**
```yaml
- process_template:
    template: 1DTEIC100Income
    amount: $EVENT_TRADE_AMOUNT * 2
    premium: ($EVENT_TRADE_NET_RESULT + $EVENT_TRADE_PREMIUM) / ($EVENT_TRADE_AMOUNT * 2)
    expiration: $EVENT_TRADE_EXPIRATION  # Optional: Verwendet das Verfallsdatum des auslösenden Trades
    time: "15:00 EST"  # Optional: Template wird erst um 15:00 Uhr EST prozessiert
```

**Hinweis zum expiration-Parameter:**
Wenn `expiration` angegeben wird, hat dieser Vorrang vor dem DTE-Wert des Templates. Dies ermöglicht beispielsweise das "Rollover" eines Trades zum gleichen Verfallsdatum wie der geschlossene Trade.

**Hinweis zum time-Parameter:**
Wenn `time` angegeben wird, wird das Template nicht sofort, sondern zur angegebenen Zeit prozessiert. Der Zeitstring wird bereits beim Laden der Konfiguration geparst und validiert - ungültige Zeitformate führen zur Deaktivierung des Flows. Wenn die Zeit in der Vergangenheit liegt, wird das Template sofort ausgeführt.

## Konfiguration

Flows werden im Abschnitt `flows` der `config.yaml` konfiguriert:

```yaml
flows:
  flow_id:
    name: "Beschreibender Name des Flows"
    enabled: true  # Optional, Standard: true
    event:
      type: early_exit  # Event-Typ
      template: 0DTEIC100Income  # Template-Name (Pflicht)
    actions:
      - send_notification:
          message: "Flow wurde ausgelöst"
          type: INFO
      - process_template:
          template: 1DTEIC100Income
          amount: 2
          premium: 0.6
```

### Vollständiges Beispiel

```yaml
flows:
  iic_rollover1:
    name: "1. Roll of 0DTE IC 100 Income to 1DTE IC 100 Income"
    enabled: true
    event:
      type: early_exit
      template: 0DTEIC100Income
    actions:
      - send_notification:
          message: "Rollover 0DTEIC100Income ausgelöst."
      - process_template:
          template: 1DTEIC100Income
          amount: $EVENT_TRADE_AMOUNT * 2
          premium: ($EVENT_TRADE_NET_RESULT + $EVENT_TRADE_PREMIUM) / ($EVENT_TRADE_AMOUNT * 2)
  
  iic_rollover2:
    name: "2. Roll of 0DTE IC 100 Income to 1DTE IC 100 Income (gleiche Expiration)"
    enabled: true
    event:
      type: early_exit
      template: 0DTEIC100Income
    actions:
      - send_notification:
          message: "Rollover mit gleicher Expiration ausgelöst."
      - process_template:
          template: 1DTEIC100Income
          amount: $EVENT_TRADE_AMOUNT * 2
          premium: ($EVENT_TRADE_NET_RESULT + $EVENT_TRADE_PREMIUM) / ($EVENT_TRADE_AMOUNT * 2)
          expiration: $EVENT_TRADE_EXPIRATION  # Verwendet das Verfallsdatum des geschlossenen Trades
  
  iic_delayed_rollover:
    name: "3. Verzögerter Rollover um 15:00 Uhr"
    enabled: true
    event:
      type: early_exit
      template: 0DTEIC100Income
    actions:
      - send_notification:
          message: "Rollover wird um 15:00 Uhr EST ausgeführt."
      - process_template:
          template: 1DTEIC100Income
          amount: $EVENT_TRADE_AMOUNT * 2
          premium: 0.65
          time: "15:00 EST"  # Template wird erst um 15:00 Uhr prozessiert
```

## Ausdrücke und Berechnungen

In den Parametern `amount`, `premium` und `expiration` der `process_template`-Action können mathematische Ausdrücke und Variablen verwendet werden:

- **Variablen**: Verwende `$EVENT_TRADE_*` Variablen
- **Operatoren**: `+`, `-`, `*`, `/`, `(`, `)`
- **Funktionen**: Alle von `simpleeval` unterstützten Funktionen (z.B. `abs()` für Absolutwerte)

**Wichtig**: Bei der Verwendung von Variablen in Ausdrücken verwende Unterstriche (`_`) statt Bindestrichen (`-`):
- ✅ Richtig: `$EVENT_TRADE_AMOUNT`
- ❌ Falsch: `$EVENT-TRADE-AMOUNT`

### Beispiele für Berechnungen

**Amount verdoppeln:**
```yaml
amount: $EVENT_TRADE_AMOUNT * 2
```

**Premium mit Fees einbeziehen:**
```yaml
premium: (abs($EVENT_TRADE_NET_RESULT) + $EVENT_TRADE_PREMIUM + $EVENT_TRADE_FEES) / ($EVENT_TRADE_AMOUNT * 2)
```

**Fees bei der Premium-Berechnung berücksichtigen:**
```yaml
# Beispiel: Neue Premium = (Verlust + alte Premium + Fees) / neue Anzahl
premium: (abs($EVENT_TRADE_NET_RESULT) + $EVENT_TRADE_PREMIUM + ($EVENT_TRADE_FEES * 2)) / ($EVENT_TRADE_AMOUNT * 2)
```

**Hinweis zur `abs()` Funktion:**
Die `abs()` Funktion macht einen negativen Wert positiv, sodass Verluste korrekt in die Premium-Berechnung einfließen:
- `abs(-150)` → `150`
- `abs(150)` → `150`

### Expiration-Parameter

Der `expiration`-Parameter kann verwendet werden, um ein spezifisches Verfallsdatum für einen neuen Trade zu setzen:

- **Verwendung von Event-Daten**: `expiration: $EVENT_TRADE_EXPIRATION` - Verwendet das Verfallsdatum des auslösenden Trades
- **Priorisierung**: Wenn `expiration` gesetzt ist, hat dies Vorrang vor dem DTE-Wert des Templates
- **Datentyp**: Muss ein `datetime.date` Objekt sein
- **Implementierung**: Das Expiration-Datum wird direkt auf dem Template gesetzt (keine DTE-Umrechnung), wodurch Rundungsfehler und Probleme mit Handelstagen vermieden werden

**Anwendungsfall**: Wenn ein 0DTE Trade vorzeitig geschlossen wird und ein 1DTE Trade mit **demselben** Verfallsdatum eröffnet werden soll (statt mit dem vom DTE berechneten Verfallsdatum).

**Technische Details**: 
- Die FlowEngine setzt das Expiration-Datum über `template.set_expiration_date(expiration)`
- Der TemplateProcessorBase prüft in `composeEntryOrder()` zuerst `template.expiration_date`
- Nur wenn `expiration_date` nicht gesetzt ist, wird die DTE-basierte Berechnung verwendet

### Time-Parameter (Verzögerte Ausführung)

Der `time`-Parameter ermöglicht die verzögerte Ausführung eines Templates zu einem bestimmten Zeitpunkt:

- **Format**: `"HH:MM <Timezone>"` (z.B. `"15:00 EST"`, `"09:30 EST"`)
- **Unterstützte Zeitzonen**: Alle von `pytz` unterstützten Zeitzonen (hauptsächlich EST, UTC)
- **Validierung beim Config-Laden**: Das Zeitformat wird bereits beim Laden der Config validiert - ungültige Formate führen zur Deaktivierung des Flows
- **Zeit in Vergangenheit**: Wenn die angegebene Zeit in der Vergangenheit liegt, wird das Template sofort ausgeführt (statt Fehler)
- **Notifications**:
  - ✅ **Erfolg**: Info-Notification mit Job-Details bei erfolgreichem Scheduling (nur bei Zeit in Zukunft)

**Anwendungsfall**: 
- Ein Trade wird um 9:30 Uhr durch Early Exit geschlossen
- Das neue Template soll aber erst um 15:00 Uhr prozessiert werden
- Ermöglicht z.B. Warten auf bessere Marktbedingungen oder höhere Prämien

**Beispiel:**
```yaml
- process_template:
    template: 1DTEIC100Income
    amount: 2
    premium: 0.65
    time: "15:00 EST"  # Wird um 15:00 Uhr Eastern Time ausgeführt
```

**Verhalten:**
- **Zeit in Zukunft** → Template wird zur angegebenen Zeit prozessiert + Info-Notification
- **Zeit in Vergangenheit** → Template wird sofort prozessiert (wie ohne `time`-Parameter)
- **Ungültiges Format** → Flow wird beim Config-Laden deaktiviert + Error-Log

**Validierung beim Startup:**
Der `time`-Parameter wird bereits beim Laden der Konfiguration validiert. Wenn ein ungültiges Zeitformat angegeben wird:
1. Fehlermeldung im Log
2. Der betroffene Flow wird automatisch deaktiviert
3. Keine Error-Notification zur Laufzeit

## Fehlverhalten

- **Fehlerhafte Action**: Wenn eine Action fehlschlägt, wird eine Error-Notification gesendet und der Flow abgebrochen
- **Parallele Flows**: Mehrere Flows können vom gleichen Event ausgelöst werden und laufen parallel
- **Deaktivierte Templates**: Wenn das in `process_template` referenzierte Template deaktiviert ist, wird die Action übersprungen
- **Fehlende Flows**: Wenn keine Flows konfiguriert sind, ist das eine gültige Konfiguration - es wird kein Fehler erzeugt
- **Ungültiges Zeitformat**: Flow wird beim Config-Laden deaktiviert (keine Runtime-Error)
- **Zeit in Vergangenheit**: Template wird sofort ausgeführt (keine Error)

## Architektur

```
FlowEngine (Singleton)
  ├── Event Handlers (eventkit)
  │   ├── early_exit_event
  │   ├── trade_opened_event
  │   ├── stop_loss_hit_event
  │   └── take_profit_hit_event
  │
  ├── Flow Execution (AsyncIOScheduler)
  │   └── Sequential Action Processing
  │
  └── Actions
      ├── send_notification
      └── process_template
```

## Logging

Die FlowEngine loggt alle wichtigen Events:

- `INFO`: Flow-Auslösung, erfolgreiche Ausführung
- `DEBUG`: Event-Emission, Action-Details
- `ERROR`: Fehler bei Flow-Ausführung oder Action-Verarbeitung
- `WARN`: Übersprungene Actions (z.B. deaktiviertes Template)

## Best Practices

1. **Eindeutige Flow-IDs**: Verwende sprechende und eindeutige IDs für Flows
2. **Namen vergeben**: Gib Flows aussagekräftige Namen zur besseren Identifikation
3. **Error Handling**: Flows werden bei Fehlern automatisch abgebrochen, plane entsprechend
4. **Template-Validierung**: Stelle sicher, dass referenzierte Templates existieren und aktiviert sind
5. **Expression-Testing**: Teste komplexe Berechnungsformeln vor dem Produktiveinsatz
6. **Notifications**: Nutze Notifications zur Überwachung der Flow-Ausführung
