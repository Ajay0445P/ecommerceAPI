from flask import Flask, request
from flask_cors import CORS
import sqlite3


def validate_data(data):
    if not data:
        return {"error": "Invalid Data Submission"}, 400

    if "name" not in data or "price" not in data or "category" not in data or "stock" not in data:
        return {"error": "Name, Price, Category and Stock of Product are required"}, 400
    if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
        return {"error": "Price must be a positive number"}, 400
    if not isinstance(data["stock"], int) or data["stock"] < 0:
        return {"error": "Stock must be non-negative integer"}, 400
    if not isinstance(data["name"], str):
        return {"error": "name must be an non-empty string"}, 400
    if not isinstance(data["category"], str):
        return {"error": "category must be an non-empty string"}, 400
    if not data["name"] or not data["category"]:
        return {"error": "Name, Category fields cannot be empty"}, 400


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Welcome to the e-commerce api"


@app.route('/products', methods=["GET"])
def allProducts():
    search = request.args.get("search")
    max_price = request.args.get("max_price")
    min_price = request.args.get("min_price")
    sort = request.args.get("sort")

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    if search:
        searchTerm = f"%{search}%"
        if min_price and max_price:
            if sort:
                if sort == "low":
                    try:
                        max_price = float(max_price)
                        min_price = float(min_price)

                        if max_price <= 0:
                            conn.close()
                            return {"error": "max_price must be a positive number"}, 400
                        if min_price <= 0:
                            conn.close()
                            return {"error": "min_price must be positive number"}, 400
                        if min_price > max_price:
                            conn.close()
                            return {"error": "Minimum price can't be higher than maximum price"}, 400
                        cursor.execute(
                            '''
                                        SELECT * FROM products
                                        WHERE (name LIKE ? OR category LIKE ?)
                                        AND price <= ? AND price >= ?
                                        ORDER BY price ASC
                                    ''', (searchTerm, searchTerm, max_price, min_price)

                        )
                        products = cursor.fetchall()
                        conn.close()
                    except ValueError:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                elif sort == "high":
                    try:
                        max_price = float(max_price)
                        min_price = float(min_price)
                        if max_price <= 0:
                            conn.close()
                            return {"error": "max_price must be a positive number"}, 400
                        if min_price <= 0:
                            conn.close()
                            return {"error": "min_price must be positive number"}, 400
                        if min_price > max_price:
                            conn.close()
                            return {"error": "Minimum price can't be higher than maximum price"}, 400
                        cursor.execute(
                            '''
                                        SELECT * FROM products
                                        WHERE (name LIKE ? OR category LIKE ?)
                                        AND price <= ? AND price >= ?
                                        ORDER BY price DESC
                                    ''', (searchTerm, searchTerm, max_price, min_price)

                        )
                        products = cursor.fetchall()
                        conn.close()
                    except ValueError:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                else:
                    conn.close()
                    return {"error": "sort must only be high or low"}, 400
            else:
                try:
                    max_price = float(max_price)
                    min_price = float(min_price)
                    if max_price <= 0:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                    if min_price <= 0:
                        conn.close()
                        return {"error": "min_price must be positive number"}, 400
                    if min_price > max_price:
                        conn.close()
                        return {"error": "Minimum price can't be higher than maximum price"}, 400
                    cursor.execute(
                        '''
                                    SELECT * FROM products
                                    WHERE (name LIKE ? OR category LIKE ?)
                                    AND price <= ? AND price >= ?
                                ''', (searchTerm, searchTerm, max_price, min_price)

                    )
                    products = cursor.fetchall()
                    conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
        elif max_price:
            if sort:
                if sort == "low":
                    try:
                        max_price = float(max_price)
                        if max_price <= 0:
                            conn.close()
                            return {"error": "max_price must be a positive number"}, 400
                        else:
                            cursor.execute(
                                '''
                                            SELECT * FROM products
                                            WHERE (name LIKE ? OR category LIKE ?)
                                            AND price <=?
                                            ORDER BY price ASC
                                        ''', (searchTerm, searchTerm, max_price,)

                            )
                            products = cursor.fetchall()
                            conn.close()
                    except ValueError:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                elif sort == "high":
                    try:
                        max_price = float(max_price)
                        if max_price <= 0:
                            conn.close()
                            return {"error": "max_price must be a positive number"}, 400
                        else:
                            cursor.execute(
                                '''
                                            SELECT * FROM products
                                            WHERE (name LIKE ? OR category LIKE ?)
                                            AND price <=?
                                            ORDER BY price DESC
                                        ''', (searchTerm, searchTerm, max_price,)

                            )
                            products = cursor.fetchall()
                            conn.close()
                    except ValueError:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                else:
                    conn.close()
                    return {"error": "sort must only be high or low"}, 400
            else:
                try:
                    max_price = float(max_price)
                    if max_price <= 0:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                    else:
                        cursor.execute(
                            '''
                                            SELECT * FROM products
                                            WHERE (name LIKE ? OR category LIKE ?)
                                            AND price <=?
                                        ''', (searchTerm, searchTerm, max_price,)

                        )
                        products = cursor.fetchall()
                        conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "max_price must be a positive number"}, 400
        elif min_price:
            if sort:
                if sort == "low":
                    try:
                        min_price = float(min_price)
                        if min_price <= 0:
                            conn.close()
                            return {"error": "min_price must be a positive number"}, 400
                        else:
                            cursor.execute(
                                '''
                                            SELECT * FROM products
                                            WHERE (name LIKE ? OR category LIKE ?)
                                            AND price >=?
                                            ORDER BY price ASC
                                        ''', (searchTerm, searchTerm, min_price,)

                            )
                            products = cursor.fetchall()
                            conn.close()
                    except ValueError:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                elif sort == "high":
                    try:
                        min_price = float(min_price)
                        if min_price <= 0:
                            conn.close()
                            return {"error": "min_price must be a positive number"}, 400
                        else:
                            cursor.execute(
                                '''
                                            SELECT * FROM products
                                            WHERE (name LIKE ? OR category LIKE ?)
                                            AND price >=?
                                            ORDER BY price DESC
                                        ''', (searchTerm, searchTerm, min_price,)

                            )
                            products = cursor.fetchall()
                            conn.close()
                    except ValueError:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                else:
                    conn.close()
                    return {"error": "sort must only be high or low"}, 400
            else:
                try:
                    min_price = float(min_price)
                    if min_price <= 0:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                    else:
                        cursor.execute(
                            '''
                                        SELECT * FROM products
                                        WHERE (name LIKE ? OR category LIKE ?)
                                        AND price >=?
                                    ''', (searchTerm, searchTerm, min_price,)

                        )
                        products = cursor.fetchall()
                        conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
        elif sort:
            if sort == "low":

                cursor.execute(
                    '''
                        SELECT * FROM products
                        WHERE (name LIKE ? OR category LIKE ?)
                        ORDER BY price ASC
                    ''', (searchTerm, searchTerm)

                )
                products = cursor.fetchall()
                conn.close()
            elif sort == "high":
                cursor.execute(
                    '''
                        SELECT * FROM products
                        WHERE (name LIKE ? OR category LIKE ?)
                        ORDER BY price DESC
                    ''', (searchTerm, searchTerm)

                )
                products = cursor.fetchall()
                conn.close()
            else:
                conn.close()
                return {"error": "sort must be high or low"}, 400

        else:
            cursor.execute(
                '''
                    SELECT * FROM products
                    WHERE (name LIKE ? OR category LIKE ?)
                ''', (searchTerm, searchTerm)

            )
            products = cursor.fetchall()
            conn.close()
    elif min_price and max_price:
        if sort:
            if sort == "low":
                try:
                    max_price = float(max_price)
                    min_price = float(min_price)

                    if max_price <= 0:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                    if min_price <= 0:
                        conn.close()
                        return {"error": "min_price must be positive number"}, 400
                    if min_price > max_price:
                        conn.close()
                        return {"error": "Minimum price can't be higher than maximum price"}, 400
                    cursor.execute(
                        '''
                            SELECT * FROM products
                            WHERE price <= ? AND price >= ?
                            ORDER BY price ASC
                        ''', (max_price, min_price)

                    )
                    products = cursor.fetchall()
                    conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
            elif sort == "high":
                try:
                    max_price = float(max_price)
                    min_price = float(min_price)
                    if max_price <= 0:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                    if min_price <= 0:
                        conn.close()
                        return {"error": "min_price must be positive number"}, 400
                    if min_price > max_price:
                        conn.close()
                        return {"error": "Minimum price can't be higher than maximum price"}, 400
                    cursor.execute(
                        '''
                            SELECT * FROM products
                            WHERE price <= ? AND price >= ?
                            ORDER BY price DESC
                        ''', (max_price, min_price)

                    )
                    products = cursor.fetchall()
                    conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
            else:
                conn.close()
                return {"error": "sort must only be high or low"}, 400
        else:
            try:
                max_price = float(max_price)
                min_price = float(min_price)
                if max_price <= 0:
                    conn.close()
                    return {"error": "max_price must be a positive number"}, 400
                if min_price <= 0:
                    conn.close()
                    return {"error": "min_price must be positive number"}, 400
                if min_price > max_price:
                    conn.close()
                    return {"error": "Minimum price can't be higher than maximum price"}, 400
                cursor.execute(
                    '''
                        SELECT * FROM products
                        WHERE price <= ? AND price >= ?
                    ''', (max_price, min_price)

                )
                products = cursor.fetchall()
                conn.close()
            except ValueError:
                conn.close()
                return {"error": "min_price must be a positive number"}, 400

    elif max_price:
        if sort:
            if sort == "low":
                try:
                    max_price = float(max_price)
                    if max_price <= 0:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                    else:
                        cursor.execute(
                            '''
                                SELECT * FROM products
                                WHERE price <=?
                                ORDER BY price ASC
                            ''', (max_price,)

                        )
                        products = cursor.fetchall()
                        conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "max_price must be a positive number"}, 400
            elif sort == "high":
                try:
                    max_price = float(max_price)
                    if max_price <= 0:
                        conn.close()
                        return {"error": "max_price must be a positive number"}, 400
                    else:
                        cursor.execute(
                            '''
                                SELECT * FROM products
                                WHERE price <=?
                                ORDER BY price DESC
                            ''', (max_price,)

                        )
                        products = cursor.fetchall()
                        conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "max_price must be a positive number"}, 400
            else:
                conn.close()
                return {"error": "sort must only be high or low"}, 400
        else:
            try:
                max_price = float(max_price)
                if max_price <= 0:
                    conn.close()
                    return {"error": "max_price must be a positive number"}, 400
                else:
                    cursor.execute(
                        '''
                                SELECT * FROM products
                                WHERE price <=?
                            ''', (max_price,)

                    )
                    products = cursor.fetchall()
                    conn.close()
            except ValueError:
                conn.close()
                return {"error": "max_price must be a positive number"}, 400
    elif min_price:
        if sort:
            if sort == "low":
                try:
                    min_price = float(min_price)
                    if min_price <= 0:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                    else:
                        cursor.execute(
                            '''
                                SELECT * FROM products
                                WHERE price >=?
                                ORDER BY price ASC
                            ''', (min_price,)

                        )
                        products = cursor.fetchall()
                        conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
            elif sort == "high":
                try:
                    min_price = float(min_price)
                    if min_price <= 0:
                        conn.close()
                        return {"error": "min_price must be a positive number"}, 400
                    else:
                        cursor.execute(
                            '''
                                SELECT * FROM products
                                WHERE price >=?
                                ORDER BY price DESC
                            ''', (min_price,)

                        )
                        products = cursor.fetchall()
                        conn.close()
                except ValueError:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
            else:
                conn.close()
                return {"error": "sort must only be high or low"}, 400
        else:
            try:
                min_price = float(min_price)
                if min_price <= 0:
                    conn.close()
                    return {"error": "min_price must be a positive number"}, 400
                else:
                    cursor.execute(
                        '''
                            SELECT * FROM products
                            WHERE price >=?
                        ''', (min_price,)

                    )
                    products = cursor.fetchall()
                    conn.close()
            except ValueError:
                conn.close()
                return {"error": "min_price must be a positive number"}, 400

    else:
        if sort:
            if sort == "low":

                cursor.execute(
                    '''
                    SELECT * FROM products
                    ORDER BY price ASC
                    '''

                )

                products = cursor.fetchall()
                conn.close()
            elif sort == "high":
                cursor.execute(
                    '''
                        SELECT * FROM products
                        ORDER BY price DESC
                    '''

                )

                products = cursor.fetchall()
                conn.close()
            else:
                conn.close()
                return {"error": "sort must only be high or low"}, 400
        else:
            cursor.execute(
                '''
                    SELECT * FROM products
                '''

            )

            products = cursor.fetchall()
            conn.close()

    product_list = []
    for product in products:
        p = {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "category": product[3],
            "stock": product[4]
        }
        product_list.append(p)
    return product_list


@app.route('/products/<int:id>', methods=["GET"])
def getoneproduct(id):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
            SELECT * FROM products WHERE id = ?
        ''', (id,)

    )
    product = cursor.fetchone()
    conn.close()
    if product:

        product_details = {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "category": product[3],
            "stock": product[4]
        }
        return product_details
    else:
        return {"error": "No product found"}, 404


@app.route('/products', methods=["POST"])
def addProduct():
    data = request.get_json()
    result = validate_data(data)
    if result:
        return result
    name = data["name"]
    price = data["price"]
    category = data["category"]
    stock = data["stock"]

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
            INSERT INTO products (name, price, category, stock) VALUES (?,?,?,?)
        ''', (name, price, category, stock)
    )
    conn.commit()
    conn.close()
    return {"message": "Product added successfully"}


@app.route('/products/<int:id>', methods=["PUT"])
def updateProduct(id):
    data = request.get_json()
    result = validate_data(data)
    if result:
        return result
    name = data["name"]
    price = data["price"]
    category = data["category"]
    stock = data["stock"]

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
            UPDATE products
            SET name = ?, price = ?, category = ?, stock = ?
            WHERE id = ?
        ''', (name, price, category, stock, id)

    )
    row = cursor.rowcount

    if row:
        conn.commit()
        conn.close()
        return {"message": "Update Successful"}
    else:
        conn.close()
        return {"error": "Product not found"}, 404


@app.route('/products/<int:id>', methods=["DELETE"])
def deleteProduct(id):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
            DELETE FROM products WHERE id =?
        ''', (id,)

    )
    row = cursor.rowcount

    if row:
        conn.commit()
        conn.close()
        return {"message": "Product deleted Successfully"}
    else:
        conn.close()
        return {"error": "Product doesn't exists"}, 404


@app.route('/cart', methods=["POST"])
def addproductcart():
    data = request.get_json()
    if not data:
        return {"error": "invalid data Submission"}, 400
    if not "product_id" in data or not "quantity" in data:
        return {"error": "Product key and Quantity are required"}, 400

    if not isinstance(data["quantity"], int) or data["quantity"] <= 0:
        return {"error": "Quantity must be a posititve integer"}, 400

    id = data["product_id"]
    reqQuantity = data["quantity"]

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
            SELECT * FROM products WHERE id = ?
        ''', (id,)

    )
    product = cursor.fetchone()
    if not product:
        conn.close()
        return {"error": "Item doesn't exists"}, 404

    if reqQuantity > product[4]:
        conn.close()
        return {"error": "products not available in the required quantity"}, 400
    else:
        cursor.execute(
            '''
                    SELECT * FROM cart WHERE product_id = ?
                ''', (id,)

        )
        row = cursor.fetchone()
        if row:
            existingQuantity = row[2]
            newQuantity = existingQuantity + reqQuantity
            if newQuantity > product[4]:
                conn.close()
                return {"error": "products not available in the required quantity"}, 400
            cursor.execute(
                '''
                    UPDATE cart
                    SET quantity = ?
                    WHERE product_id = ?
                ''', (newQuantity, id)

            )
            conn.commit()
            conn.close()
            return {"message": "product added to the cart"}
        else:
            cursor.execute(
                '''
                    INSERT INTO cart (product_id, quantity) VALUES (?,?)
                ''', (id, reqQuantity)

            )
            conn.commit()
            conn.close()
            return {"message": "product added to the cart"}


@app.route('/cart', methods=["GET"])
def getcart():
    conn = sqlite3.connect("ecommerce.db")

    cursor = conn.cursor()

    cursor.execute(
        '''
            SELECT cart.product_id,
            cart.quantity,
            products.name,
            products.price
            FROM cart
            JOIN products
            ON cart.product_id = products.id;
        '''

    )
    data = cursor.fetchall()
    if not data:
        conn.close()
        return {"message": "cart is empty"}
    total = 0
    cart = []
    for row in data:
        id = row[0]
        quantity = row[1]
        name = row[2]
        price = row[3]
        subtotal = quantity * price
        total += subtotal

        cartproducts = {
            "product_id": id,
            "quantity": quantity,
            "name": name,
            "price": price,
            "subtotal": subtotal
        }
        cart.append(cartproducts)
    result = {
        "cart": cart,
        "total": total
    }

    conn.close()

    return result


@app.route('/cart/<int:product_id>', methods=["DELETE"])
def deletecartproduct(product_id):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(
        '''
            DELETE FROM cart
            WHERE product_id = ?
        ''', (product_id,)
    )
    row = cursor.rowcount
    if row:
        conn.commit()
        conn.close()
        return {"message": "Deleted Successfully"}
    else:
        conn.close()
        return {"error": "product doesn't exists"}, 404


@app.route('/cart/<int:product_id>', methods=["PATCH"])
def updatecart(product_id):
    data = request.get_json()
    if not data:
        return {"error": "quantity is required"}, 400
    if "quantity" not in data:
        return {"error": "quantity is required"}, 400

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(
        '''
            SELECT * FROM cart
            WHERE product_id = ?
        ''', (product_id,)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"product doesn't exists"}, 404

    if not isinstance(data["quantity"], int) or data["quantity"] <= 0:
        conn.close()
        return {"Quantity mmust be positive integer"}, 400
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if product:
        if data["quantity"] > product[4]:
            conn.close()
            return {"error": "product is not available in the required quantity"}, 400
    else:
        conn.close()
        return {"error": "product doesn't exists"}, 404
    cursor.execute(
        '''
                UPDATE cart
                SET quantity = ?
                WHERE product_id = ?
            ''', (data["quantity"], product_id)

    )
    conn.commit()
    conn.close()
    return {"message": "updated successfully"}


app.run(debug=True)
