# Frontend Documentation

The frontend is a React application built with Vite and TypeScript. It serves as the interface for Doctors to manage patients, view SOAP notes, and configure greetings.

## Setup & Installation

1. **Dependencies**
    Navigate to the frontend directory and install dependencies:

    ```bash
    npm install
    ```

    *Note: If dependency conflicts arise due to React 19, use `npm install --legacy-peer-deps`.*

2. **Environment Variables**
    Create a `.env` file in the `frontend` root:

    ```env
    VITE_API_URL=http://localhost:8000
    VITE_WS_URL=ws://localhost:8000
    ```

## Running the Application

Start the development server:

```bash
npm run dev
