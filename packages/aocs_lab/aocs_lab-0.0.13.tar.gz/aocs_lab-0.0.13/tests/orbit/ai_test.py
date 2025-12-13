from mcp.server.fastmcp import FastMCP
import repeat

mcp = FastMCP()

@mcp.tool(description="获取回归轨道列表, 输入期望的轨道高度(单位米), 返回高度在该值上下50公里范围内的回归轨道列表")
def get_repeat_orbit(height: float) -> str:
    res = repeat.repeat_orbit_search(
        height - 50e3, 
        height + 50e3, 
        0, 100, 
        50, 500)

    text = "高度km    e        倾角deg  回归圈数  回归天数\n"
    for r in res:
        text = text + (f"{r[0]:8.2f} {r[1]:15.5e} {r[2]:9.4f} {r[3]:7d} {r[4]:7d}\n")

    return text



if __name__ == "__main__":
    mcp.run(transport="streamable-http")



