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
            Active color: <input type="color" name="color" value="#{color}"><br/>
            Background color: <input type="color" name="background_color" value="#{background_color}"><br/>
            Animation delay: <input type="range" list="tickmarks" name="delay" min=5 max=500 step=5 value="{delay}">
            <datalist id="tickmarks">
                <option value="5" label="min"></option>
                <option value="100" label="default"></option>
                <option value="500" label="max"></option>
            </datalist>
        <script>
            async function onChange(e) {{
                try {{
                    const value = e.target.value;
                    const param = e.target.name;
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
            document.querySelectorAll("input").forEach(
                (el) => el.addEventListener('change', (e) => onChange(e))
            );
        </script>
    </body>
</html>
"""