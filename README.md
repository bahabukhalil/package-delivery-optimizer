# Package Delivery Optimizer

This project implements **optimization strategies for local package delivery operations** using **Simulated Annealing** and **Genetic Algorithm**. It was developed as part of **ENCS3340 Project #1 (Second Semester 2024/25)** at Birzeit University.

The system assigns packages to delivery vans and determines optimal routes to minimize total distance while respecting van capacities and package priorities.

---

### 🚀 Features
- Two AI-based optimization algorithms: **Simulated Annealing** and **Genetic Algorithm**
- Interactive **Streamlit** web interface
- Dynamic plotting of delivery routes
- Input options: generate random data or upload structured `.txt` files
- Adjustable algorithm parameters:
  - *Simulated Annealing:* cooling rate (0.90 - 0.99)
  - *Genetic Algorithm:* population size (50 - 100), mutation rate (0.01 - 0.1)

---

### 📂 Project Structure

| File | Description |
|-------|-------------|
| `app.py` | Streamlit app interface |
| `main.py` | Entry point script |
| `models.py` | Data models and utilities |
| `genetic_algorithm.py` | Genetic Algorithm solver |
| `simulated_annealing.py` | Simulated Annealing solver |
| `case1.txt`, `case2.txt`, `case3.txt` | Example input files |

---

### 🛠 Installation & Running

#### 1️⃣ Clone the repository
```bash
git clone https://github.com/bahabukhahil/package-delivery-optimizer.git
cd package-delivery-optimizer
```

#### 2️⃣ Install dependencies
You can manually install:
```bash
pip install streamlit matplotlib numpy pandas Pillow
```
Or create a `requirements.txt`:
```
streamlit
matplotlib
numpy
pandas
Pillow
```
Then install:
```bash
pip install -r requirements.txt
```

#### 3️⃣ Run the application
```bash
python main.py
```
or
```bash
streamlit run app.py
```

#### 4️⃣ Open in browser
Go to: `http://localhost:8501`

---

### 📊 How to Use

✅ **Choose input method:**  
- *Generate random data* → specify vans & parcels  
- *Upload file* → structured `.txt` files (see example format below)  

✅ **Choose algorithm:**  
- *Genetic Algorithm* → set population size, mutation rate  
- *Simulated Annealing* → set cooling rate  

✅ **Run optimization:**  
Click **Run Optimization** and view:
- Total distance
- Parcel assignments
- Van usage
- Route plot

✅ **Download results:**  
Use the **Download CSV** button to export the optimized parcel data.

---

### 📎 Example Input Format (`.txt`)
```
<Van count>
<ID capacity>
...

<Parcel count>
<ID X Y Weight Priority>
...
```
Example:
```
2
0 100
1 150

3
0 10.0 10.0 20.0 1
1 50.0 50.0 30.0 2
2 70.0 20.0 25.0 3
```

---

### 🧠 Algorithms

#### Simulated Annealing
- Initial temperature: 1000  
- Cooling rate: user input (0.90 - 0.99)  
- Stopping temp: 1  
- Iterations per temp: 100  

#### Genetic Algorithm
- Population size: user input (50 - 100)  
- Mutation rate: user input (0.01 - 0.1)  
- Generations: 500  

---

### 👨‍💻 Author

**Baha Abu Khalil**  
[LinkedIn](https://www.linkedin.com/in/baha-abu-khalil)

---

### ⚠ License

Academic use only — developed for coursework at Birzeit University.
