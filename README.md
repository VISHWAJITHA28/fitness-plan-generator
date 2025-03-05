# fitness-plan-generator
Here's a **README.md** file for your **Fitness Plan Generator** project. This README includes a project overview, setup instructions, and key features.  


 🏋️‍♂️ Fitness Plan Generator 🚀

A **data-driven personalized fitness plan generator** that dynamically adjusts workouts, nutrition, and progress tracking based on **Google Fit** and manual user inputs.

📌 Features
✅ **Personalized Workout Plans** based on age, weight, health conditions  
✅ **Meal Tracking & Nutrition Logging**  
✅ **Weight Tracking** with visual progress charts 📊  
✅ **Google Fit API Integration** for real-time fitness data 🏃‍♂️  
✅ **User-friendly UI** using **Streamlit**  

---

## ⚙️ **Tech Stack**
- **Backend:** Flask (Python), SQLite, Google Fit API  
- **Frontend:** Streamlit (Python), Matplotlib  
- **APIs Used:** Google Fit API, Fitbit (optional)  

---

## 🛠 **Setup Instructions**
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/fitness-plan-generator.git
cd fitness-plan-generator
```

### 2️⃣ Install Dependencies
#### **Backend:**
```sh
cd backend
pip install -r requirements.txt
python backend.py  # Start Flask server
```

#### **Frontend:**
```sh
cd ../frontend
pip install -r requirements.txt
streamlit run frontend.py  # Start Streamlit UI
```

---

## 🔗 **Google Fit API Setup**
1️⃣ **Enable Google Fit API** on [Google Cloud Console](https://console.cloud.google.com/)  
2️⃣ **Create OAuth credentials** and get your `CLIENT_ID` & `CLIENT_SECRET`  
3️⃣ **Set up Redirect URI** → `http://localhost:5000/callback`  
4️⃣ **Run Flask & Log in** via `http://localhost:5000/login`  

---

## 🚀 **How It Works**
1️⃣ **Users log in & connect Google Fit API**  
2️⃣ **Personalized workout plan is generated** based on health conditions  
3️⃣ **Users can log meals & weight progress**  
4️⃣ **Google Fit syncs steps & calories data** for insights  

---

## 🎯 **Next Improvements**
🔹 AI-based workout recommendations 🤖  
🔹 Integration with **Apple Health** & more APIs  
🔹 Mobile App version 📱  

---

## 📜 **License**
This project is **open-source** under the **MIT License**.

---

## 👨‍💻 **Contributors**
👤 Byru vishwajitha | GitHub: [vishwajitha28](https://github.com/vishwajitha28)  
