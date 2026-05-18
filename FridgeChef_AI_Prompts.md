# FRIDGECHEF: AI ASSISTANT PROMPTS
These documents are designed to be copy-pasted into AI coding assistants like Cursor, Claude Code, GitHub Copilot, or ChatGPT. They are written in English to ensure the highest quality of generated code.

---

# DOCUMENT 1: BACKEND PROMPT (Django + DRF)

**System Role:** You are an Expert Senior Backend Developer specializing in Python, Django, and Django REST Framework (DRF).
**Task:** Build the backend REST API for a monolithic web application called "FridgeChef". This app allows users to input ingredients they have and uses an AI API to generate a recipe.

### 1. Technology Stack
- **Framework:** Django 4.x + Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** Django Session Authentication (Cookies). DO NOT use JWT.
- **Environment:** Use `python-dotenv` for env variables.
- **CORS:** Use `django-cors-headers`. Configure it to allow credentials (`CORS_ALLOW_CREDENTIALS = True`).

### 2. Database Schema (Models)
Create an app named `recipes`. We will use the default Django `User` model for authentication.
Create a `Recipe` model with the following fields:
- `user`: ForeignKey to `auth.User`, on_delete=CASCADE, related_name='recipes'
- `title`: CharField, max_length=255
- `ingredients_used`: TextField (to store the list of ingredients)
- `instructions`: TextField (step-by-step cooking guide)
- `prep_time_minutes`: IntegerField
- `created_at`: DateTimeField, auto_now_add=True

### 3. API Endpoints
Implement the following endpoints. Use standard DRF Serializers and Views/ViewSets. All endpoints must prefix with `/api/`.

**Auth Endpoints (Session-based):**
- `POST /api/auth/register/` - Register a new user (username, email, password).
- `POST /api/auth/login/` - Login user and set session cookie.
- `POST /api/auth/logout/` - Logout user and clear session.
- `GET /api/auth/me/` - Return current logged-in user data.

**Recipe Endpoints:**
- `GET /api/recipes/` - List all recipes saved by the authenticated user.
- `POST /api/recipes/` - Save a generated recipe to the database (User must be authenticated).
- `GET /api/recipes/<id>/` - Retrieve a specific recipe.
- `DELETE /api/recipes/<id>/` - Delete a specific recipe.

**AI Generation Endpoint:**
- `POST /api/recipes/generate/`
  - **Payload:** `{"ingredients": ["egg", "tomato", "cheese"]}`
  - **Action:** Take the ingredients, build a text prompt, and call the OpenAI API (or a mock function if API key is not provided).
  - **Prompt logic:** "You are a chef. I have these ingredients: {ingredients}. Generate a simple recipe. Return ONLY valid JSON with keys: 'title' (string), 'instructions' (string), 'prep_time_minutes' (int)."
  - **Response:** Return the parsed JSON directly to the frontend. DO NOT save it to the database automatically.

### 4. Constraints & Rules
- Do not overengineer. Keep views simple.
- Implement basic error handling (400 for bad inputs, 401/403 for auth errors).
- Ensure CSRF protection is configured correctly for a decoupled React frontend.
- Provide clear setup instructions (e.g., `requirements.txt`).

---

# DOCUMENT 2: FRONTEND PROMPT (React + Vite)

**System Role:** You are an Expert Senior Frontend Developer specializing in React and TailwindCSS.
**Task:** Build a Single Page Application (SPA) for "FridgeChef" that connects to a Django REST API.

### 1. Technology Stack
- **Framework:** React 18+ (initialized via Vite)
- **Styling:** TailwindCSS
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **Icons:** Lucide React or Heroicons

### 2. Architecture & Setup
- Configure Axios globally. VERY IMPORTANT: Set `axios.defaults.withCredentials = true` so session cookies are sent to the Django backend.
- Handle Django's CSRF token by extracting the `csrftoken` cookie and attaching it to the `X-CSRFToken` header for POST/PUT/DELETE requests.
- Create a clear folder structure: `/components`, `/pages`, `/services`, `/hooks`.

### 3. Pages & UI Requirements
Design a clean, minimal, mobile-first interface. Use a light theme with food-related accent colors (e.g., orange or green).

**A. Authentication Pages (`/login`, `/register`)**
- Simple centered forms. Include email/username and password fields.
- Redirect to Home (`/`) on successful login.

**B. Home / Generator Page (`/`)**
- **Hero Section:** Catchy title and a brief description.
- **Input Area:** A text input where users can type ingredients and press Enter to add them as "tags" or "chips".
- **Action Button:** "Generate Recipe". Must show a loading spinner/state while waiting for the AI response.
- **Result Area:** Once the API responds, render a visually appealing Card showing the `title`, `prep_time_minutes`, and `instructions`. Include a "Save Recipe" button.

**C. Dashboard Page (`/dashboard`)**
- Requires authentication (protect this route).
- Display a CSS Grid of `RecipeCard` components showing all user-saved recipes.
- Include a "Delete" icon/button on each card.

### 4. Constraints & Rules
- Create reusable components (e.g., `Button`, `Input`, `RecipeCard`).
- Manage user auth state globally (using React Context or simple state at the root level) so the Navbar can toggle between "Login" and "Dashboard/Logout".
- Handle loading and error states gracefully (e.g., display a toast or error message if the API fails).
- Write modern React code: use functional components, hooks (`useState`, `useEffect`), and avoid class components.
