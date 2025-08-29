import { Input } from "@/components/ui/input.jsx"
import { Button } from "@/components/ui/button.jsx"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Sun, Moon } from "lucide-react"
import { useState } from "react"
import Typewriter from "typewriter-effect"
import axios from "axios"
import PageLoader from "./PageLoader"

function FakeNewsChecker() {

    const [query, setQuery] = useState("")
    const [verdict, setVerdict] = useState("")
    const [summary, setSummary] = useState("")
    const [reasoning, setReasoning] = useState("")
    const [sources, setSources] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    const [isDark, setIsDark] = useState(document.documentElement.classList.contains("dark"));

    // function to handle the check button click
    const handleCheck = async (e) => {

        e.preventDefault()

        if (!query.trim()){
            return;
        }

        try {
            setIsLoading(true)

            const res = await axios.post("http://localhost:8009/news", {
                query: query,
            });

            setIsLoading(false);
            setQuery("")

            console.log("Data received from backend is: " , res)
            const msg = res.data.response;

            // const msg = "Verdict: True  \nReason: The headline states that a \"president implemented national emergency,\" which aligns with multiple verified instances where U.S. presidents have declared national emergencies, including President Trump in 2019, 2020, and 2025. However, the headline lacks specificity (e.g., which president, which emergency), making it partially true. The web data confirms such declarations occurred but does not validate an exact match to the vague headline.  \n\nSummary: U.S. presidents, including Trump, have declared national emergencies, such as the Southern Border emergency (February 15, 2019, renewed in 2020 and January 20, 2025). The headline is partially accurate but lacks details.  \n\nSources: Tavily (referencing National Emergencies Act, 1976; Trump's 2019, 2020, and 2025 declarations)."
            // const msg= "Verdict: False  \nReason: The headline \"i am spiderman\" does not refer to a real-world event or verifiable claim. The web search data only discusses fictional and metaphorical references to Spider-Man from media (e.g., movies, music, comic lore) and does not provide evidence of an actual occurrence. No credible sources confirm a factual basis for the headline.  \n\nSummary: null  \nSources: Columbia Records (music), Marvel Comics-related content  \n\nNote: The search results pertain to entertainment contexts rather than real-world events, reinforcing the lack of authenticity."       

            const verdictMatch = msg.match(/Verdict:\s*(.+?)\s{2,}/);
            const reasonMatch = msg.match(/Reason:\s*([\s\S]*?)\n\s*\n/);
            const summaryMatch = msg.match(/Summary:\s*(.+?)\s{2,}/);
            const sourcesMatch = msg.match(/Sources:\s*([\s\S]*?)$/m);

            const verdict = verdictMatch?.[1]?.trim() || "Unknown";
            const reasoning = reasonMatch?.[1]?.trim() || "No reasoning available.";
            const sources = sourcesMatch?.[1]?.trim() || "No sources available.";

            let summaryRaw = summaryMatch?.[1]?.trim() || "";
            const summary = summaryRaw.toLowerCase() === "null" || summaryRaw == "" ? "No summary available" : summaryRaw;

            console.log({ verdict, reasoning, summary, sources });

            setVerdict(verdict);
            setReasoning(reasoning);
            setSummary(summary);
            setSources(sources)

        } catch (err) {
            console.error("Error checking headline:", err);
            setVerdict("Error");
            setReasoning("Failed to fetch response from server.");
            setSummary("Please try again later.");
            setSources("No sources available")
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

        isLoading? 
        (<PageLoader/>) : 
        (
            <div className="text-foreground max-w-4xl mx-auto p-6 space-y-6 ">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold dark:text-gray-100">
                    Fake News Detector
                </h1>
                
                {/* -------toogle theme button ------ */}
                <div className="flex items-center space-x-2">
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
                    <span className={verdict === "Partially True" || verdict === 'True' ? "text-green-400" : "text-red-400"}>
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
                        strings:[sources || 'Sources will appear here after checking.'],
                        autoStart: true,
                        delay: 35,
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
                            delay: 30,
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
                            delay: 30,
                            deleteSpeed: Infinity,
                            cursor: "",
                        }}
                        
                    />
                </div>

            </div>

        </div>
        )
        
    )
}

export { FakeNewsChecker };
