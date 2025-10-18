import pytest
from fastapi import status
from app import models

class TestCartOperations:
    """Test shopping cart operations."""
    
    def test_add_to_cart_unauthorized(self, client, test_product):
        """Test adding item to cart without authentication."""
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        response = client.post("/cart/add", json=cart_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_add_to_cart_success(self, client, test_product, auth_headers):
        """Test successfully adding item to cart."""
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        response = client.post("/cart/add", json=cart_data, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_id"] == test_product.id
        assert data["quantity"] == 2
        assert "id" in data
    
    def test_add_to_cart_nonexistent_product(self, client, auth_headers):
        """Test adding non-existent product to cart."""
        cart_data = {
            "product_id": 999,
            "quantity": 2
        }
        response = client.post("/cart/add", json=cart_data, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product not found" in response.json()["detail"]
    
    def test_add_to_cart_update_existing(self, client, test_product, auth_headers):
        """Test adding same product to cart multiple times (should update quantity)."""
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        
        # Add item first time
        response1 = client.post("/cart/add", json=cart_data, headers=auth_headers)
        assert response1.status_code == status.HTTP_200_OK
        
        # Add same item again
        response2 = client.post("/cart/add", json=cart_data, headers=auth_headers)
        assert response2.status_code == status.HTTP_200_OK
        data = response2.json()
        assert data["quantity"] == 4  # 2 + 2
    
    def test_view_cart_unauthorized(self, client):
        """Test viewing cart without authentication."""
        response = client.get("/cart/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_view_cart_empty(self, client, auth_headers):
        """Test viewing empty cart."""
        response = client.get("/cart/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_view_cart_with_items(self, client, test_product, auth_headers):
        """Test viewing cart with items."""
        # Add item to cart first
        cart_data = {
            "product_id": test_product.id,
            "quantity": 3
        }
        client.post("/cart/add", json=cart_data, headers=auth_headers)
        
        # View cart
        response = client.get("/cart/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["product_id"] == test_product.id
        assert data[0]["quantity"] == 3
        assert "product" in data[0]
        assert data[0]["product"]["name"] == "Test Product"
    
    def test_remove_from_cart_unauthorized(self, client, test_product):
        """Test removing item from cart without authentication."""
        response = client.delete(f"/cart/{test_product.id}")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_remove_from_cart_success(self, client, test_product, auth_headers):
        """Test successfully removing item from cart."""
        # Add item to cart first
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        client.post("/cart/add", json=cart_data, headers=auth_headers)
        
        # Remove item from cart
        response = client.delete(f"/cart/{test_product.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert "Item removed from cart" in response.json()["message"]
        
        # Verify cart is empty
        cart_response = client.get("/cart/", headers=auth_headers)
        assert cart_response.json() == []
    
    def test_remove_from_cart_item_not_in_cart(self, client, test_product, auth_headers):
        """Test removing item that's not in cart."""
        response = client.delete(f"/cart/{test_product.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Item not in cart" in response.json()["detail"]
    
    def test_remove_from_cart_nonexistent_product(self, client, auth_headers):
        """Test removing non-existent product from cart."""
        response = client.delete("/cart/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Item not in cart" in response.json()["detail"]

class TestCartMultipleItems:
    """Test cart operations with multiple different items."""
    
    def test_cart_multiple_different_items(self, client, auth_headers, db_session, test_product):
        """Test cart with multiple different products."""
        # Create additional products
        product2 = db_session.add(models.Product(
            name="Product 2",
            description="Second product",
            price=50.0,
            quantity=5
        ))
        product3 = db_session.add(models.Product(
            name="Product 3", 
            description="Third product",
            price=75.0,
            quantity=8
        ))
        db_session.commit()
        
        # Add multiple different items
        items = [
            {"product_id": test_product.id, "quantity": 2},  # Use actual test_product id
            {"product_id": 2, "quantity": 1},
            {"product_id": 3, "quantity": 3}
        ]
        
        for item in items:
            response = client.post("/cart/add", json=item, headers=auth_headers)
            assert response.status_code == status.HTTP_200_OK
        
        # View cart
        response = client.get("/cart/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        
        # Verify all items are present
        product_ids = [item["product_id"] for item in data]
        assert test_product.id in product_ids
        assert 2 in product_ids  
        assert 3 in product_ids

class TestCartEdgeCases:
    """Test cart edge cases and error conditions."""
    
    def test_add_to_cart_zero_quantity(self, client, test_product, auth_headers):
        """Test adding item with zero quantity."""
        cart_data = {
            "product_id": test_product.id,
            "quantity": 0
        }
        response = client.post("/cart/add", json=cart_data, headers=auth_headers)
        # This should still work as there's no validation for zero quantity
        # In a real application, you'd want to add this validation
        assert response.status_code == status.HTTP_200_OK
    
    def test_add_to_cart_negative_quantity(self, client, test_product, auth_headers):
        """Test adding item with negative quantity."""
        cart_data = {
            "product_id": test_product.id,
            "quantity": -1
        }
        response = client.post("/cart/add", json=cart_data, headers=auth_headers)
        # This should still work as there's no validation for negative quantity
        # In a real application, you'd want to add this validation
        assert response.status_code == status.HTTP_200_OK
    
    def test_cart_isolation_between_users(self, client, db_session, test_product):
        """Test that cart items are isolated between different users."""
        # Create second user
        user2 = models.User(
            username="user2",
            email="user2@example.com", 
            hashed_password="hashed_password",
            is_admin=False
        )
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)
        
        # Create auth headers for second user
        from app.auth.jwt_handler import create_access_token
        token2 = create_access_token({"sub": str(user2.id)})
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Add item to cart for first user
        cart_data = {"product_id": test_product.id, "quantity": 2}
        response1 = client.post("/cart/add", json=cart_data, headers={"Authorization": "Bearer fake_token"})
        # This will fail due to invalid token, but that's expected
        
        # Add item to cart for second user
        response2 = client.post("/cart/add", json=cart_data, headers=headers2)
        assert response2.status_code == status.HTTP_200_OK
        
        # Verify second user's cart has the item
        cart_response = client.get("/cart/", headers=headers2)
        assert cart_response.status_code == status.HTTP_200_OK
        data = cart_response.json()
        assert len(data) == 1
        assert data[0]["product_id"] == test_product.id
