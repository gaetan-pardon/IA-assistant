import { useState, useEffect } from "react";
import { verifyToken } from "../../services/UserService";
import { Link, useNavigate } from "react-router-dom"


export function ProtectedRoute({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    
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
        navigate("/login");
        return null;
    }
    return children;
}
