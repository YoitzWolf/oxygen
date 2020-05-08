class SvgMaster:
        def getSvg(filename):
            with open(filename, "r") as svg: return svg.read()
            
        def getFullLogo():
            with open("./static/logo/logo_full_mono.svg", "r") as svg: return svg.read()
        