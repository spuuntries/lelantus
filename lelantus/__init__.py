from colorama import Fore, Style, init
import minify_html
import os

init()


def embed(html: str, image: str, out: str = None, minify: bool = True):
    """
    Embed the HTML into the image.

    Arguments
    ---------
    html : str
           A path to an HTML file to inject into the image.
    image : str
            A path to a JPEG file to inject into.

    Keyword Arguments
    -----------------
    out : str
          (Optional) A path to write the injected file to.
    minify : bool
          (Optional) Whether to minify the HTML prior to injection.
          NOTE: this also minifies the JS and CSS
    """
    if not os.path.isfile(html):
        raise FileNotFoundError(html)
    if not os.path.isfile(image):
        raise FileNotFoundError(image)

    with open(image, "rb") as f:
        content = f.read()
        if content[:3] != b"\xff\xd8\xff":
            raise Exception("Non-JPEG image detected.")

    with open(html, encoding="utf8") as f:
        to_inject = f.read()

    if minify:
        to_inject = minify_html.minify(to_inject, minify_js=True, minify_css=True)

    injected = (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00--><!--head-->"
        + b"<script>document.body.innerHTML=document.body.innerHTML.split('<!--head-->')[1]</script>"
        + bytes(to_inject, "utf8")
        + b'<script type="text/javascript"></body></html>'
    )

    headt_idx = content.find(b"\xff\xdb")
    con_wohead = content[headt_idx:]
    appended = injected + con_wohead

    if len(injected) > 10000:
        print(
            f"{Fore.YELLOW}[WARN]{Style.RESET_ALL}: Resulting header is larger than 10 kb, there's a possibility of deletion by content publishers!".upper()
        )

    if out:
        with open(out, "wb") as f:
            f.write(appended)

    return appended


__all__ = ["embed"]
