Store: 

Tabla de Empleados:

## ID (Clave primaria)
Nombre
Apellido
Cargo
Departamento
Correo electrónico
Contraseña (para el acceso a la tienda interna)
Tabla de Productos:

## ID (Clave primaria)
Nombre del producto
Descripción
Precio
Categoría
Stock (cantidad disponible en el inventario)

## Tabla de Pedidos:
ID (Clave primaria)
ID del empleado (Clave externa que hace referencia a la tabla de Empleados)
Fecha del pedido
Estado del pedido (por ejemplo, pendiente, completado, en proceso)
Total del pedido

Tabla de Detalles del Pedido:

ID del detalle del pedido (Clave primaria)
ID del pedido (Clave externa que hace referencia a la tabla de Pedidos)
ID del producto (Clave externa que hace referencia a la tabla de Productos)
Cantidad
Subtotal (precio por unidad * cantidad)
Tabla de Historial de Compras:

ID (Clave primaria)
ID del empleado (Clave externa que hace referencia a la tabla de Empleados)
ID del pedido (Clave externa que hace referencia a la tabla de Pedidos)
Fecha de compra
Tabla de Categorías de Productos (si es aplicable):

ID (Clave primaria)
Nombre de la categoría