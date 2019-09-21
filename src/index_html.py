html = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
    <head> <title>Neopixel googles configuration</title> </head>
    <body> 
        <h1>Configuration page</h1>
        <h2>You can choose program and color</h2>
            <input type="radio" name="program" value="1" {is1checked}> Cycle <br>
            <input type="radio" name="program" value="2" {is2checked}> Bounce <br>
            <input type="radio" name="program" value="3" {is3checked}> Fade <br>
            Color: <input type="color" name="color" value="#{color}">
        <script>
            async function onChange(e, param) {{
                try {{
                    const value = e.target.value;
                    result = await fetch('/', {{
                        method: 'POST',
                        body: JSON.stringify({{[param]: value}})
                    }})
                }} catch (error) {{
                    e.preventDefault();
                    console.error(error);
                    alert("Something went wrong, check console for details!");
                }}
            }}
            document.querySelectorAll("[name=program]").forEach(
                (el) => el.addEventListener('change', (e) => onChange(e, 'program'))
            );
            document.querySelectorAll("[name=color]").forEach(
                (el) => el.addEventListener('change', (e) => onChange(e, 'color'))
            );
        </script>
    </body>
</html>
"""