# Portal académico de Carlos Molina

Prueba inicial de sitio estático para GitHub Pages.

## Publicación recomendada

La cuenta de GitHub es:

```text
CarlosMH712
```

Para publicar el portal como sitio principal, crea un repositorio público llamado exactamente:

```text
CarlosMH712.github.io
```

Después sube estos archivos a la raíz de la rama `main`:

- `index.html`
- `styles.css`
- `script.js`

En GitHub:

1. Abre el repositorio.
2. Entra a `Settings`.
3. Selecciona `Pages`.
4. En `Build and deployment`, elige `Deploy from a branch`.
5. Selecciona la rama `main` y la carpeta `/ (root)`.
6. Guarda la configuración.

El portal deberá quedar disponible en:

```text
https://CarlosMH712.github.io
```

## Calculadora de Streamlit

La tarjeta de flujo compresible tiene un enlace provisional. Cuando la calculadora se publique en Streamlit Community Cloud, sustituye en `index.html`:

```html
href="#"
```

por la dirección pública de la aplicación, por ejemplo:

```html
href="https://nombre-de-la-app.streamlit.app"
```

y elimina las clases y atributos de estado deshabilitado si corresponde.
