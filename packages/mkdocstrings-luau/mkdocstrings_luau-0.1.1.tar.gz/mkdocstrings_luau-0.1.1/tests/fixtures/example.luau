-- Example Luau module
-- This is a sample module for testing

-- Add two numbers together
-- Returns the sum of a and b
function add(a: number, b: number): number
    return a + b
end

-- Subtract one number from another
function subtract(x: number, y: number): number
    return x - y
end

-- Greet someone by name
-- If no name is provided, uses "World"
function greet(name: string)
    print("Hello, " .. name)
end
