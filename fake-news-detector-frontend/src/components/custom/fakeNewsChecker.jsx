import { Input } from "@/components/ui/input.jsx"
import { Button } from "@/components/ui/button.jsx"
import {useState} from "react"

function FakeNewsChecker() {

    const [query, setQuery] = useState("")
    const [verdict, setVerdict] = useState("")
    const [summary, setSummary] = useState("")
    const [reasoning, setReasoning] = useState("")


    // function to handle the check button click
    const handleCheck = () => {
        if (query.toLowerCase().includes("fake")) {
            setVerdict("Fake")
            setSummary("This news appears to be misleading, lacking credible sources or verified data. The content uses emotionally charged language and presents claims without supporting evidence, raising strong suspicion of misinformation.")
            setReasoning("The article contains exaggerated statements and no official references. It exhibits classic patterns of fake news, including manipulation tactics, anonymous sources, and the absence of factual consistency with established reports.")
        } else {
            setVerdict("Valid")
            setSummary("The news seems genuine and aligns with facts reported by multiple reputable sources. The language is neutral and the information is well-structured, reflecting a high degree of reliability and clarity.")
            setReasoning("Verified news outlets and official reports back the claim. The article includes accurate data, quotes from known sources, and follows journalistic standards, indicating it is authentic and trustworthy.")
        }
    }


  return (

    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold dark:text-gray-100">
        Fake News Detector
      </h1>

        {/** ------- input field for user to enter news or statement------ */} 
        <div className="space-y-2">
            <label
                htmlFor="news-query"
                className="block text-sm font-medium text-white dark:text-white"
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
        </div>

        {/* ------- Check Button -------- */}
        <div>
            <Button 
            variant="light" 
            onClick={handleCheck} 
            >
                Check News
            </Button>
        </div>

        {/* ------- Show Verdict Below Button ------ */}
        {verdict && (
            <div className="mt-4 text-lg font-semibold text-white">
            Verdict:{" "}
            <span className={verdict === "Fake" ? "text-red-400" : "text-green-400"}>
                {verdict}
            </span>
            </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
        {/* Summary Block */}
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
                    Summary
                </h2>
                <p className="text-gray-700 dark:text-gray-300">
                    {summary || "Summary will appear here after checking."}
                </p>
            </div>

            {/* Reasoning Block */}
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
                    Reasoning
                </h2>
                <p className="text-gray-700 dark:text-gray-300">
                    {reasoning || "Reasoning will appear here after checking."}
                </p>
            </div>
        </div>


    </div>
  )
}

export {FakeNewsChecker};
