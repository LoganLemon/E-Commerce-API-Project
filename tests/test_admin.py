import pytest
from fastapi import status

class TestAdminProductManagement:
    """Test admin product management endpoints."""
    
    def test_create_product_unauthorized(self, client):
        """Test creating product without authentication."""
        product_data = {
            "name": "Admin Product",
            "description": "A product created by admin",
            "price": 199.99,
            "quantity": 10
        }
        response = client.post("/admin/products", json=product_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_product_regular_user(self, client, auth_headers):
        """Test creating product as regular user (should fail)."""
        product_data = {
            "name": "Regular User Product",
            "description": "A product created by regular user",
            "price": 99.99,
            "quantity": 5
        }
        response = client.post("/admin/products", json=product_data, headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admins only" in response.json()["detail"]
    
    def test_create_product_admin_success(self, client, admin_headers):
        """Test creating product as admin user."""
        product_data = {
            "name": "Admin Created Product",
            "description": "A product created by admin",
            "price": 299.99,
            "quantity": 20
        }
        response = client.post("/admin/products", json=product_data, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Admin Created Product"
        assert data["price"] == 299.99
        assert data["quantity"] == 20
        assert "id" in data
    
    def test_get_all_products_unauthorized(self, client):
        """Test getting all products without authentication."""
        response = client.get("/admin/products")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_all_products_regular_user(self, client, auth_headers):
        """Test getting all products as regular user (should fail)."""
        response = client.get("/admin/products", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admins only" in response.json()["detail"]
    
    def test_get_all_products_admin_success(self, client, admin_headers, test_product):
        """Test getting all products as admin user."""
        response = client.get("/admin/products", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert any(product["name"] == "Test Product" for product in data)
    
    def test_update_product_unauthorized(self, client, test_product):
        """Test updating product without authentication."""
        update_data = {
            "name": "Updated Product",
            "price": 150.0
        }
        response = client.put(f"/admin/products/{test_product.id}", json=update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_product_regular_user(self, client, test_product, auth_headers):
        """Test updating product as regular user (should fail)."""
        update_data = {
            "name": "Updated Product",
            "price": 150.0
        }
        response = client.put(f"/admin/products/{test_product.id}", json=update_data, headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admins only" in response.json()["detail"]
    
    def test_update_product_admin_success(self, client, test_product, admin_headers):
        """Test updating product as admin user."""
        update_data = {
            "name": "Updated Test Product",
            "price": 150.0,
            "quantity": 15
        }
        response = client.put(f"/admin/products/{test_product.id}", json=update_data, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Test Product"
        assert data["price"] == 150.0
        assert data["quantity"] == 15
    
    def test_update_product_partial(self, client, test_product, admin_headers):
        """Test partial update of product."""
        update_data = {
            "name": "Partially Updated Product"
            # Only updating name, other fields should remain unchanged
        }
        response = client.put(f"/admin/products/{test_product.id}", json=update_data, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Partially Updated Product"
        assert data["price"] == test_product.price  # Should remain unchanged
        assert data["quantity"] == test_product.quantity  # Should remain unchanged
    
    def test_update_product_not_found(self, client, admin_headers):
        """Test updating non-existent product."""
        update_data = {
            "name": "Updated Product",
            "price": 150.0
        }
        response = client.put("/admin/products/999", json=update_data, headers=admin_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product not found" in response.json()["detail"]
    
    def test_delete_product_unauthorized(self, client, test_product):
        """Test deleting product without authentication."""
        response = client.delete(f"/admin/products/{test_product.id}")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_product_regular_user(self, client, test_product, auth_headers):
        """Test deleting product as regular user (should fail)."""
        response = client.delete(f"/admin/products/{test_product.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admins only" in response.json()["detail"]
    
    def test_delete_product_admin_success(self, client, test_product, admin_headers):
        """Test deleting product as admin user."""
        response = client.delete(f"/admin/products/{test_product.id}", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        assert "Product deleted" in response.json()["detail"]
        
        # Verify product is deleted
        get_response = client.get(f"/products/{test_product.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_product_not_found(self, client, admin_headers):
        """Test deleting non-existent product."""
        response = client.delete("/admin/products/999", headers=admin_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product not found" in response.json()["detail"]

class TestAdminValidation:
    """Test admin endpoint validation."""
    
    def test_create_product_missing_fields(self, client, admin_headers):
        """Test creating product with missing required fields."""
        product_data = {
            "name": "Incomplete Product"
            # Missing description, price, quantity
        }
        response = client.post("/admin/products", json=product_data, headers=admin_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_product_invalid_data_types(self, client, admin_headers):
        """Test creating product with invalid data types."""
        product_data = {
            "name": "Invalid Product",
            "description": "A product with invalid data types",
            "price": "not_a_number",  # Should be a number
            "quantity": "not_a_number"  # Should be a number
        }
        response = client.post("/admin/products", json=product_data, headers=admin_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_product_invalid_data_types(self, client, test_product, admin_headers):
        """Test updating product with invalid data types."""
        update_data = {
            "price": "not_a_number",  # Should be a number
            "quantity": "not_a_number"  # Should be a number
        }
        response = client.put(f"/admin/products/{test_product.id}", json=update_data, headers=admin_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestAdminEdgeCases:
    """Test admin endpoint edge cases."""
    
    def test_admin_endpoints_with_invalid_token(self, client, test_product):
        """Test admin endpoints with invalid authentication token."""
        headers = {"Authorization": "Bearer invalid_token"}
        
        # Test all admin endpoints with invalid token
        response1 = client.get("/admin/products", headers=headers)
        assert response1.status_code == status.HTTP_401_UNAUTHORIZED
        
        response2 = client.post("/admin/products", json={}, headers=headers)
        assert response2.status_code == status.HTTP_401_UNAUTHORIZED
        
        response3 = client.put(f"/admin/products/{test_product.id}", json={}, headers=headers)
        assert response3.status_code == status.HTTP_401_UNAUTHORIZED
        
        response4 = client.delete(f"/admin/products/{test_product.id}", headers=headers)
        assert response4.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_admin_endpoints_without_token(self, client, test_product):
        """Test admin endpoints without authentication token."""
        # Test all admin endpoints without token
        response1 = client.get("/admin/products")
        assert response1.status_code == status.HTTP_403_FORBIDDEN
        
        response2 = client.post("/admin/products", json={})
        assert response2.status_code == status.HTTP_403_FORBIDDEN
        
        response3 = client.put(f"/admin/products/{test_product.id}", json={})
        assert response3.status_code == status.HTTP_403_FORBIDDEN
        
        response4 = client.delete(f"/admin/products/{test_product.id}")
        assert response4.status_code == status.HTTP_403_FORBIDDEN
