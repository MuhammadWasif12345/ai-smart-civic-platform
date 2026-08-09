// --------------------------------------------------------------------------------
// API WRAPPER (api.js)
// This file handles secure communication with our backend for admin pages.
// It automatically attaches the JWT login token to every request, and automatically
// redirects the admin back to the login page if their session expires.
// --------------------------------------------------------------------------------

class ApiClient {
  
  static getToken() {
    // We store the login token in the browser's localStorage
    return localStorage.getItem("admin_token");
  }

  static setToken(token) {
    localStorage.setItem("admin_token", token);
  }

  static clearToken() {
    localStorage.removeItem("admin_token");
  }

  static async fetchSecure(endpoint, options = {}) {
    const token = this.getToken();
    
    // If there is no token, the admin isn't logged in. Boot them to the login page.
    if (!token) {
      window.location.href = "admin-login.html";
      return null;
    }

    // Set up the headers, injecting the JWT token as a Bearer token
    const headers = {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
      ...(options.headers || {})
    };

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(endpoint, config);
      
      // 401 Unauthorized means the token expired or is invalid
      if (response.status === 401) {
        this.clearToken();
        alert("Your session expired — please log in again.");
        window.location.href = "admin-login.html";
        return null;
      }
      
      return response;
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      throw error;
    }
  }
}
