
import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import { verifyToken } from "../../services/UserService";

export function ProtectedRoute({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function checkAuth() {
            try {
                const response = await verifyToken();
                if (response.status === 200) {
                    setIsAuthenticated(true);
                } else {
                    setIsAuthenticated(false);
                }
            } catch (error) {
                setIsAuthenticated(false);
            } finally {
                setLoading(false);
            }  
        }
        checkAuth();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    } else if (!isAuthenticated) {
        return {/* <Navigate to="/login" /> */};
    }
    return children;
}
