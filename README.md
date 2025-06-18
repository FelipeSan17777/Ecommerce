# Design Shop

**Design Shop** es una tienda en línea desarrollada con el framework **Django** (Python 3.12), enfocada en ofrecer una experiencia fluida tanto para clientes como para administradores. Actualmente utiliza **SQLite** como base de datos, pero está preparada para migrar fácilmente a **MySQL** mediante XAMPP.

---

## Características Principales

- Registro e inicio de sesión de usuarios
- Visualización de productos por categorías
- Carrito de compras
- Panel de administración personalizado
- Gestión de productos y categorías (solo para admins)
- Sistema de plantillas con Bootstrap y HTML5
- Panel adaptable para distintos tipos de usuario

---

## Tecnologías Utilizadas

| Tecnología | Versión | Descripción |
|-----------|---------|-------------|
| Python    | 3.12    | Lenguaje principal del backend |
| Django    | 4.x     | Framework web de alto nivel |
| SQLite    | nativa  | Base de datos por defecto en desarrollo |
| XAMPP     | 8.x     | Para usar Apache/MySQL si se desea migrar |
| HTML/CSS  | -       | Diseño del frontend |
| Bootstrap | 5.x     | Estilos responsivos y componentes UI |

---

## Instalación y Configuración

###  Como hacerlo funcionar

```
descargar e instalar xampp para posteriormente correrlo
-- bash
git clone https://github.com/tuusuario/design-shop.git
cd Ecommerce
pip install django
python manage.py runserver
