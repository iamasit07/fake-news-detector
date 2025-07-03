import { Input } from "@/components/ui/input.jsx"
import { Button } from "@/components/ui/button.jsx"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Sun, Moon } from "lucide-react"
import { useState } from "react"
import Typewriter from "typewriter-effect"
import axios from "axios"

function FakeNewsChecker() {

    const [query, setQuery] = useState("")
    const [verdict, setVerdict] = useState("")
    const [summary, setSummary] = useState("")
    const [reasoning, setReasoning] = useState("")
    const [isDark, setIsDark] = useState(document.documentElement.classList.contains("dark"));

    // function to handle the check button click
    const handleCheck = async (e) => {

        e.preventDefault()

        if (!query.trim()){
            return;
        }

        try {
            const res = await axios.post("http://localhost:8080/news", {
                query: query,
            });

            setQuery("")

            console.log("Data received from backend is: " , res)
            const msg = res.data.msg;
                   
            const verdictMatch = msg.match(/is \*\*(\w+)\*\*/);
            const reasoningMatch = msg.match(/\*\*Reasoning\*\*:\s*([\s\S]*?)\n\s*\n/);
            const summaryMatch = msg.match(/\*\*Summary\*\*:([\s\S]*?)\n\n/);

            const verdict = verdictMatch?.[1] || "Unknown";
            const reasoning = reasoningMatch?.[1] || "No reasoning available.";
            const summary = summaryMatch?.[1] || "No summary available.";

            setVerdict(verdict);
            setReasoning(reasoning);
            setSummary(summary);
        } catch (err) {
            console.error("Error checking headline:", err);
            setVerdict("Error");
            setReasoning("Failed to fetch response from server.");
            setSummary("Please try again later.");
        }
    };


    //toogle theme function
    const toggleTheme = (value) => {
        setIsDark(value);
        if (value) {
            document.documentElement.classList.add("dark")
        } else {
            document.documentElement.classList.remove("dark")
        }
    }



    return (

        <div className="text-foreground max-w-4xl mx-auto p-6 space-y-6 ">
            <h1 className="text-2xl font-bold dark:text-gray-100">
                Fake News Detector
            </h1>

            {/** ------- input field for user to enter news or statement------ */}
            <form 
            onSubmit={handleCheck}
            className="space-y-2">
                <label
                    htmlFor="news-query"
                    className="block text-sm font-medium dark:text-white"
                >
                    Enter News
                </label>
                <Input
                    id="news-query"
                    placeholder="Enter your news or statement here"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
            </form>

            {/* ------- Check Button -------- */}
            <div>
                <Button
                    variant="outline"
                    onClick={handleCheck}
                >
                    Check News
                </Button>
            </div>

            {/* ------- Show Verdict Below Button ------ */}
            {verdict && (
                <div className="mt-4 text-lg font-semibold">
                    Verdict :{" "}
                    <span className={verdict === "Fake" ? "text-green-400" : "text-red-400"}>
                        {verdict}
                    </span>
                </div>
            )}

            {/* ------------- Sources text ------------- */}
            <div className="bg-gray-200 dark:bg-gray-800 p-4 rounded-lg shadow-lg">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
                    Sources
                </h2>

                <Typewriter 
                    className="text-gray-700 dark:text-gray-300"
                    options={{
                        strings:['Sources will appear here after checking.'],
                        autoStart: true,
                        delay: 50,
                        deleteSpeed: Infinity,
                        cursor: "",
                    }}
                    
                />
            </div>

            {/* Reasoning and Summary */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">

                {/* Reasoning Block */}
                <div className="bg-gray-200 dark:bg-gray-800 p-4 rounded-lg shadow-lg">
                    <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
                        Reasoning
                    </h2>

                    <Typewriter 
                        className="text-gray-700 dark:text-gray-300"
                        options={{
                            strings:[reasoning || 'Reasoning will appear here after checking.'],
                            autoStart: true,
                            delay: 45,
                            deleteSpeed: Infinity,
                            cursor: "",
                        }}
                        
                    />
                </div>

                {/* Summary Block */}
                <div className="bg-gray-200 dark:bg-gray-800 p-4 rounded-lg shadow-lg">
                    <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
                        Summary
                    </h2>
                    <Typewriter 
                        className="text-gray-700 dark:text-gray-300"
                        options={{
                            strings:[summary || "Summary will appear here after checking."],
                            autoStart: true,
                            delay: 45,
                            deleteSpeed: Infinity,
                            cursor: "",
                        }}
                        
                    />
                </div>

            </div>


            {/* -------toogle theme button ------ */}
            <div className="absolute top-20 right-60 flex items-center space-x-2">
                <Switch
                    id="theme-toggle"
                    onCheckedChange={toggleTheme}
                    aria-label="Toggle dark mode"
                />
                {isDark ? (
                    <Sun className="w-4 h-4 text-white" />
                ) : (
                    <Moon className="w-4 h-4 text-foreground" />
                )
                }
            </div>

        </div>
    )
}

export { FakeNewsChecker };
