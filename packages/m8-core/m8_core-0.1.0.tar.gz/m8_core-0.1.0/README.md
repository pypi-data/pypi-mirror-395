m8-core

The Official Python Client for the M8P Hypervisor.

M8P is a unified execution engine for AI Agents, combining Vector Storage, Logic, and Inference into a single high-performance runtime. m8-core allows you to orchestrate M8P sessions from Python.

Installation

pip install m8-core


Quick Start

from m8_core import M8

SESSION_ID = "my_agent_v1"

# 1. Initialize Memory
init_script = """
vdb_instance AGENT_MEM dim=4096 max_elements=10000
return "Ready"
"""
M8.EnsureExists(SESSION_ID, code=init_script)

# 2. Run Inference
script = """
store <prompt> Why is the sky blue?
llm_infer <prompt> <result>
return <result>
"""
response = M8.RunSession(SESSION_ID, script)
print(response)


Requirements

Python 3.8+

requests