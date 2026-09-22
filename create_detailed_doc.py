import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_heading(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    if level == 1:
        for run in heading.runs:
            run.font.color.rgb = RGBColor(0, 102, 51) # Dark Green
    return heading

def add_bold_para(doc, label, text):
    p = doc.add_paragraph()
    p.add_run(label).bold = True
    p.add_run(text)
    return p

doc = docx.Document()

# Title
title = doc.add_heading('AgriGo - Smart Logistics Platform', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle = doc.add_paragraph('Complete Technical Interview Notes')
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

# =========================================================
# 1. Elevator Pitch
# =========================================================
add_heading(doc, '1. Elevator Pitch')

doc.add_heading('30 Seconds Pitch:', level=2)
doc.add_paragraph("AgriGo is an Android-based smart logistics platform designed to connect farmers directly with transport drivers, field laborers, and machinery providers. Built using Java, Firebase, and Google Maps, it offers real-time GPS tracking, automated ML-based vehicle prediction, and OTP-secured job fulfillment, eliminating middlemen and optimizing agricultural supply chains.")

doc.add_heading('1 Minute Pitch:', level=2)
doc.add_paragraph("AgriGo is a comprehensive agricultural logistics solution. Farmers often struggle to find reliable transport or labor at fair prices. Our Android application solves this by providing a unified platform where farmers can book transport vehicles based on crop weight, hire manual labor for specific tasks like harvesting, or rent heavy machinery. Under the hood, it leverages Firebase Authentication for secure role-based access, Cloud Firestore for real-time dispatching and status updates, and the Google Maps SDK for live tracking of drivers. We even integrated an external Machine Learning API using Retrofit to automatically predict the most suitable transport vehicle based on crop yield.")

doc.add_heading('3 Minutes Pitch:', level=2)
doc.add_paragraph("I developed AgriGo, a robust Android application to address the logistical inefficiencies in the agricultural sector. The core problem is that farmers face significant delays and price gouging when moving crops to market or finding seasonal workers. AgriGo serves as an aggregator.")
doc.add_paragraph("The architecture is heavily reliant on Firebase. We use Firebase Auth to manage four distinct user roles: Farmers, Drivers, Laborers, and Machinery Providers. When a farmer creates a booking—say, transporting 5000kg of wheat—a background service (DriverDispatchService) broadcasts this 'transport_request' to nearby available drivers using GeoQueries and Firestore snapshot listeners. We implemented a fallback queue system so if one driver rejects, it pings the next.")
doc.add_paragraph("A standout feature is the real-time tracking. Once a driver accepts a job, we use the FusedLocationProviderClient to stream their coordinates to Firestore. The farmer's app listens to these updates, and using the Google Directions API and Google Maps SDK, we draw dynamic polylines on the map and calculate live ETAs. To ensure security and trust, the job can only be marked 'Started' once the driver enters a 4-digit OTP provided by the farmer upon arrival. We built this entirely in native Java, focusing on a responsive Material Design UI, asynchronous Firebase calls to prevent UI blocking, and clean architecture principles.")

doc.add_heading('5 Minutes Pitch:', level=2)
doc.add_paragraph("For a 5-minute pitch, expand on the 3-minute pitch by diving into technical challenges and specific implementation details:")
p = doc.add_paragraph()
p.style = 'List Bullet'
p.add_run("Discuss the ML Integration: ").bold = True
p.add_run("Explain how you used Retrofit to communicate with a Python/Render backend. Detail how the model takes crop type and weight to recommend a vehicle, saving farmers money by preventing overbooking capacity.")
p = doc.add_paragraph()
p.style = 'List Bullet'
p.add_run("Discuss Map Routing complexities: ").bold = True
p.add_run("Explain the fallback mechanism in MapUtils.java where if the Google Directions API fails or rate-limits, it gracefully falls back to the open-source OSRM routing engine to fetch polyline geometries.")
p = doc.add_paragraph()
p.style = 'List Bullet'
p.add_run("Discuss State Management: ").bold = True
p.add_run("Explain how TrackingActivity manages complex state machines (State 1: Assigned, State 2: Arrived at Pickup, State 3: On Trip, State 4: Completed) based purely on real-time Firestore document updates.")

# =========================================================
# 2. Problem Statement
# =========================================================
add_heading(doc, '2. Problem Statement')

add_bold_para(doc, "What problem existed? ", "Farmers, especially in rural areas, lack direct, reliable access to transport logistics, manual labor, and farming machinery. They rely on local brokers who charge high commissions.")
add_bold_para(doc, "Why this project was needed? ", "To digitize the agricultural supply chain. By directly connecting the service provider to the farmer, costs are reduced, and efficiency is increased.")
add_bold_para(doc, "Current problems in agriculture logistics: ", "Lack of transparency in pricing, unreliable ETAs, high spoilage rates due to delayed transport, and difficulty finding seasonal labor during peak harvest.")
add_bold_para(doc, "Why existing methods fail: ", "Traditional methods rely on word-of-mouth and phone calls to middlemen. There is no real-time tracking, no accountability, and no data-driven decision making.")
add_bold_para(doc, "Motivation behind the project: ", "To empower farmers with technology similar to ride-hailing apps (like Uber/Ola) but tailored specifically for agricultural needs (crop types, high payload weights, specific machinery).")


# =========================================================
# 3. Project Architecture
# =========================================================
add_heading(doc, '3. Project Architecture')

doc.add_paragraph("The application follows a Client-Server architecture heavily utilizing BaaS (Backend as a Service) provided by Firebase.")

doc.add_heading('ASCII Architecture Diagram:', level=2)
doc.add_paragraph("""
[ Android Client App (Java) ]
       |        |        |
   (Auth)   (Data)   (Maps/Location)
       |        |        |
       v        v        v
[ Firebase ] [ Firestore ] [ Google APIs ]
(Auth)       (NoSQL DB)    (Maps, Directions)
       |        |
       +--------+
            | (Triggers/Updates)
            v
[ ML Backend (Python/Render) ] <--- Retrofit API Call
""")

doc.add_heading('Data Flow Explanation:', level=2)
p = doc.add_paragraph()
p.add_run("1. Android App: ").bold = True
p.add_run("Acts as the presentation and logic layer. Contains distinct modules for Farmers, Drivers, and Laborers.\n")
p.add_run("2. Firebase Authentication: ").bold = True
p.add_run("Handles user sign-up/in and session management.\n")
p.add_run("3. Firestore: ").bold = True
p.add_run("The central hub. When a Farmer creates a booking, a document is written here. The Driver App has active SnapshotListeners (DriverDispatchService) watching this database.\n")
p.add_run("4. Google Maps & GPS: ").bold = True
p.add_run("The Driver App continuously fetches GPS coordinates via FusedLocationProviderClient and writes them to Firestore. The Farmer App reads these coordinates and plots them on Google Maps.\n")

# =========================================================
# 4. Complete Workflow
# =========================================================
add_heading(doc, '4. Complete Workflow')

workflow = doc.add_paragraph()
workflow.add_run("1. Registration/Login: ").bold = True
workflow.add_run("User downloads app, selects role (Farmer/Driver/Labor), enters details, and registers via Firebase.\n")
workflow.add_run("2. Create Booking: ").bold = True
workflow.add_run("Farmer opens Dashboard -> Transport Booking.\n")
workflow.add_run("3. Input Details: ").bold = True
workflow.add_run("Selects crop type from RecyclerView, enters weight in KG.\n")
workflow.add_run("4. Location Selection: ").bold = True
workflow.add_run("Uses Map to drop pins for Pickup and Destination. Reverse Geocoding translates Lat/Lng to readable addresses.\n")
workflow.add_run("5. ML Prediction / Vehicle Selection: ").bold = True
workflow.add_run("App calls external ML API (or uses local logic fallback) to recommend vehicle type and estimates price.\n")
workflow.add_run("6. Dispatch: ").bold = True
workflow.add_run("Booking saved to Firestore. DriverDispatchService alerts nearby drivers with matching vehicle types.\n")
workflow.add_run("7. Driver Accepts: ").bold = True
workflow.add_run("Driver sees IncomingRequestActivity, taps 'Accept'. Transaction locks the booking to this driver.\n")
workflow.add_run("8. Navigation & Live Tracking: ").bold = True
workflow.add_run("TrackingActivity opens. Route drawn via Directions API. Farmer tracks driver live.\n")
workflow.add_run("9. OTP Verification: ").bold = True
workflow.add_run("Driver arrives at pickup. Farmer provides 4-digit OTP shown on their screen. Driver enters it to start the trip. (Ensures security).\n")
workflow.add_run("10. Delivery & Payment: ").bold = True
workflow.add_run("Driver reaches destination, clicks 'Complete Trip'. Status updates in DB. Earnings updated.")


# =========================================================
# 5. Every Feature Explained
# =========================================================
add_heading(doc, '5. Every Feature Explained')

def feature_notes(doc, feature, what, why, how, adv, disadv, questions, logic):
    doc.add_heading(feature, level=2)
    p = doc.add_paragraph()
    p.add_run("What it is: ").bold = True; p.add_run(f"{what}\n")
    p.add_run("Why needed: ").bold = True; p.add_run(f"{why}\n")
    p.add_run("How it works: ").bold = True; p.add_run(f"{how}\n")
    p.add_run("Advantages: ").bold = True; p.add_run(f"{adv}\n")
    p.add_run("Disadvantages/Limitations: ").bold = True; p.add_run(f"{disadv}\n")
    p.add_run("Code Logic: ").bold = True; p.add_run(f"{logic}\n")
    p.add_run("Interview Question: ").bold = True; p.add_run(f"{questions}\n")

feature_notes(doc, "Firebase Authentication & Login/Registration",
              "System to verify user identity securely using email/password.",
              "To restrict unauthorized access, maintain individual profiles, and separate app functionality based on user role (Farmer vs. Driver).",
              "Uses FirebaseAuth.getInstance().createUserWithEmailAndPassword(). On success, user data (name, role, etc.) is stored in Firestore under a 'users' collection with the UID as the document ID.",
              "Secure, easy to implement, handles password hashing automatically.",
              "Requires internet connectivity.",
              "LoginActivity checks input validity using ValidationUtils, calls signInWithEmailAndPassword, then fetches the role from Firestore to route the user to the correct Dashboard.",
              "Q: How do you handle session persistence? A: Firebase Auth automatically persists the session token. I also use SharedPreferences (PreferenceManager) to cache the user's role and name locally so the app opens instantly to the dashboard.")

feature_notes(doc, "OTP Verification",
              "A 4-digit One-Time Password generated dynamically per booking.",
              "Prevents fraud. Ensures the driver has actually met the farmer and picked up the goods before the trip status changes to 'On Trip'.",
              "Generated using `new java.util.Random().nextInt(9000) + 1000` during booking creation and saved to Firestore. Only visible on Farmer's screen. Driver must input it to proceed.",
              "Simple, highly secure offline verification step between two humans.",
              "If the farmer's phone dies, they can't see the OTP.",
              "In TrackingActivity, `btnVerifyOtp.setOnClickListener` compares the EditText input against the `bookingOtp` fetched from Firestore.",
              "Q: Is the OTP secure if it's in Firestore? A: Yes, Firestore Security Rules can be configured so only the involved Farmer and Driver can read that document.")

feature_notes(doc, "Live Location Tracking & GPS",
              "Real-time plotting of the driver's geographic coordinates on the farmer's map.",
              "To provide transparency and accurate ETAs to the farmer.",
              "Driver app runs `FusedLocationProviderClient` with `Priority.PRIORITY_HIGH_ACCURACY` requesting updates every 3 seconds. It pushes `lat`/`lng` to Firestore. Farmer app has a `SnapshotListener` on the driver's document. When coordinates change, it uses `MarkerAnimationUtils.animateMarkerToGB` to smoothly glide the truck icon.",
              "Excellent UX, removes anxiety about where the truck is.",
              "High battery consumption for the driver. Susceptible to GPS dead zones.",
              "In TrackingActivity, `onLocationResult` gets the location and calls `db.collection(\"drivers\").document(uid).update(...)`. Farmer receives this via `addSnapshotListener`.",
              "Q: Why use FusedLocationProviderClient instead of the standard Android LocationManager? A: FusedLocationProvider intelligently balances battery life and accuracy by combining GPS, Wi-Fi, and cell networks, whereas LocationManager relies purely on the hardware GPS chip.")

feature_notes(doc, "Google Maps SDK & Directions API",
              "Google's mapping interface and routing service.",
              "To visualize the journey and calculate driving distance/time.",
              "Maps SDK provides the `SupportMapFragment`. `MapUtils.fetchRoute()` makes an HTTP call to the Directions API JSON endpoint. `PolyUtil.decode()` translates the returned encoded string into a List of `LatLng` points, which are drawn as a `Polyline`.",
              "Industry standard, highly accurate routing.",
              "Directions API costs money at high volumes.",
              "To save costs and prevent crashes if the API limit is hit, `MapUtils.java` has a fallback mechanism to use OSRM (Open Source Routing Machine) to fetch the route.",
              "Q: How do you draw the route on the map? A: I parse the 'overview_polyline' points from the Directions API JSON, decode it into LatLngs, and pass it to `map.addPolyline(new PolylineOptions().addAll(path))`.")

feature_notes(doc, "RecyclerView & CardView",
              "Android UI components for displaying lists of data.",
              "Used to display dynamic lists like 'Active Requests' or 'Crop Selection' efficiently without crashing the app.",
              "RecyclerView recycles view layouts (CardViews) as they scroll off-screen. It requires an Adapter (e.g., DriverRequestAdapter) and a ViewHolder.",
              "Highly memory efficient.",
              "Requires more boilerplate code than simple ListViews.",
              "Adapter inflates `item_driver_request.xml` (a CardView), binds the Firestore data (crop, weight, location) to the TextViews in `onBindViewHolder`.",
              "Q: What is the ViewHolder pattern? A: It caches the references to UI components (like TextViews) inside the layout so we don't have to call computationally expensive `findViewById()` every time a row is drawn.")


# =========================================================
# 6. Firebase (In-Depth)
# =========================================================
add_heading(doc, '6. Firebase Technical Deep Dive')

doc.add_paragraph("Firebase is the backbone of AgriGo. You must know these concepts thoroughly:")

p = doc.add_paragraph()
p.add_run("Firestore Collections & Documents: ").bold = True
p.add_run("Firestore is NoSQL. Data is stored in JSON-like 'Documents', which are grouped into 'Collections'.\n")
p.add_run("Key Collections in AgriGo: ").bold = True
p.add_run("`users`, `drivers`, `transport_requests`, `machinery_bookings`, `labor_workers`.\n")

p = doc.add_paragraph()
p.add_run("Snapshot Listeners (Real-time updates): ").bold = True
p.add_run("Instead of writing a 'while loop' to check for updates, we attach an `addSnapshotListener`. Firebase maintains an open WebSocket connection. When a document changes in the cloud, the `onEvent` method fires instantly on the Android device. This powers the Dispatch System and Live Tracking.\n")

p = doc.add_paragraph()
p.add_run("Transactions: ").bold = True
p.add_run("Used during Job Acceptance. Multiple drivers might click 'Accept' simultaneously. `db.runTransaction()` reads the status. If it's still 'REQUESTED', it changes it to 'ACCEPTED' and assigns the driver. If another driver got it first, the transaction fails safely. (See `IncomingRequestActivity.java`)\n")

p = doc.add_paragraph()
p.add_run("Offline Support: ").bold = True
p.add_run("Firestore caches data locally. If a farmer loses internet, they can still view their existing bookings. Changes made offline are queued and synced automatically when the network returns.\n")

doc.add_paragraph("Interview Q: What is the difference between Realtime Database and Firestore?").bold = True
doc.add_paragraph("Answer: Firestore is the newer version. It allows more complex queries (like querying by multiple fields without downloading the whole tree), scales better automatically, and organizes data in intuitive Collections/Documents rather than one massive JSON tree.")


# =========================================================
# 7. Android Concepts Used
# =========================================================
add_heading(doc, '7. Android Concepts Used')

p = doc.add_paragraph()
p.add_run("Activities & Lifecycles: ").bold = True
p.add_run("Every screen is an Activity. We manage resources in lifecycles (e.g., stopping GPS updates in `onPause()` to save battery, restarting in `onResume()`).\n")

p = doc.add_paragraph()
p.add_run("Intents: ").bold = True
p.add_run("Explicit Intents are used to navigate between screens (e.g., `new Intent(this, TrackingActivity.class)`). We pass data using `intent.putExtra(\"REQUEST_ID\", id)`.\nImplicit Intents are used to open external apps, like clicking 'Call Driver' fires `new Intent(Intent.ACTION_DIAL, Uri.parse(\"tel:...\"))`.\n")

p = doc.add_paragraph()
p.add_run("Foreground Services: ").bold = True
p.add_run("`DriverDispatchService.java` is a Foreground Service. It displays a persistent notification. This allows the app to listen for incoming transport requests and track location even if the driver minimizes the app.\n")

p = doc.add_paragraph()
p.add_run("Runtime Permissions: ").bold = True
p.add_run("Used for Location access. App uses `ActivityCompat.requestPermissions()` and handles the result in `onRequestPermissionsResult()`.\n")

# =========================================================
# 8. Challenges Faced & Solutions
# =========================================================
add_heading(doc, '8. Realistic Challenges & Solutions')

ch1 = doc.add_paragraph()
ch1.add_run("Challenge 1: Google Directions API Rate Limits/Costs.\n").bold = True
ch1.add_run("Solution: ").bold = True
ch1.add_run("Implemented a dual-routing system in `MapUtils.java`. It tries Google API first. If it fails or is rate-limited, it automatically falls back to OSRM (Open Source Routing Machine), a free alternative. Also throttled route recalculation in TrackingActivity to maximum once every 10 seconds.\n")

ch2 = doc.add_paragraph()
ch2.add_run("Challenge 2: Concurrency - Multiple drivers accepting the same job.\n").bold = True
ch2.add_run("Solution: ").bold = True
ch2.add_run("Used Firestore Transactions. It ensures atomic reads and writes. It checks if `status == 'REQUESTED'` and updates it. If two drivers hit it at the exact millisecond, the server rejects one.\n")

ch3 = doc.add_paragraph()
ch3.add_run("Challenge 3: Jumpy/Erratic Map Markers during Live Tracking.\n").bold = True
ch3.add_run("Solution: ").bold = True
ch3.add_run("GPS coordinates jump abruptly. Created `MarkerAnimationUtils.java` using Android's `ValueAnimator`. It interpolates the points and smoothly glides the marker from point A to point B over 2.5 seconds, while also calculating the spherical bearing to rotate the truck icon to face the correct direction.\n")


# =========================================================
# 9. Future Enhancements
# =========================================================
add_heading(doc, '9. Future Enhancements')
p = doc.add_paragraph()
p.style = 'List Bullet'
p.add_run("Digital Payments Integration: ").bold = True
p.add_run("Integrating Razorpay or Stripe to allow cashless transactions and escrow payments.")
p = doc.add_paragraph()
p.style = 'List Bullet'
p.add_run("Multi-Language Support: ").bold = True
p.add_run("Adding Regional languages (Hindi, Telugu, etc.) using Android's `strings.xml` localization framework to increase rural accessibility.")
p = doc.add_paragraph()
p.style = 'List Bullet'
p.add_run("Price Bidding System: ").bold = True
p.add_run("Instead of fixed prices, allow farmers to input a budget, and drivers can counter-offer or accept.")


doc.save(r'C:\Users\DELL\Documents\SATHISH\AGRIGO\AgriGo_Interview_Notes.docx')
print("Complete Interview Notes generated successfully!")
