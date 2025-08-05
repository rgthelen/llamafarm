import { useState } from 'react'
import FontIcon from '../common/FontIcon'

const Prompt = () => {
  const [hasGeneratedOutputs, setHasGeneratedOutputs] = useState(false)
  const [activeTab, setActiveTab] = useState('evaluate')

  const tempOutputs = [
    {
      output:
        'A pressure drop in the hydraulic pump during taxi on an F-16 could be caused by fluid leakage, air in the system, or a failing pressure sensor. Recommended next steps include inspecting hydraulic lines for leaks, checking fluid levels, and running a diagnostic on the pressure sensor.',
      tag: 'tag here',
    },
    {
      output:
        'Check for leaks or sensor issues. You may need to replace the pump.',
      tag: 'tag here',
    },
    {
      output:
        'This issue is likely due to avionics interference. Reset the flight computer and continue the mission.',
      tag: 'tag here',
    },
  ]

  const RateOutput = ({ output, tag }: { output: string; tag: string }) => {
    const [isThumbsUpFilled, setIsThumbsUpFilled] = useState(false)
    const [isThumbsDownFilled, setIsThumbsDownFilled] = useState(false)

    return (
      <div
        className={`flex flex-col border-[1px] border-solid border-blue-400 rounded-lg p-4 gap-2 ${
          isThumbsUpFilled ? 'border-green-100' : ''
        }`}
      >
        <div className="flex flex-row gap-2 justify-between">
          <div>{output}</div>
          <div className="flex flex-row gap-2 ml-4">
            <FontIcon
              type={isThumbsUpFilled ? 'thumbs-up-filled' : 'thumbs-up'}
              className="w-6 h-6"
              isButton
              handleOnClick={() => {
                setIsThumbsUpFilled(!isThumbsUpFilled)
                setIsThumbsDownFilled(false)
              }}
            />
            <FontIcon
              type={isThumbsDownFilled ? 'thumbs-down-filled' : 'thumbs-down'}
              className="w-6 h-6"
              isButton
              handleOnClick={() => {
                setIsThumbsDownFilled(!isThumbsDownFilled)
                setIsThumbsUpFilled(false)
              }}
            />
          </div>
        </div>
        <div className="w-fit py-1 px-3 bg-blue-600 rounded-2xl text-sm">
          {tag}
        </div>
      </div>
    )
  }

  if (hasGeneratedOutputs) {
    return (
      <div className="w-full flex flex-col gap-2 mb-4">
        <div>Prompt</div>
        <div className="flex flex-row mb-4">
          <div className="w-full flex flex-row">
            <button
              className={`border-b-2 border-solid ${
                activeTab === 'evaluate'
                  ? 'border-green-100'
                  : 'border-blue-600'
              } pb-1 pl-4 w-full text-left`}
              onClick={() => setActiveTab('evaluate')}
            >
              Evaluate
            </button>
            <button
              className={`border-b-2 border-solid ${
                activeTab === 'prompt' ? 'border-green-100' : 'border-blue-600'
              } pb-1 pl-4 w-full text-left`}
              onClick={() => setActiveTab('prompt')}
            >
              Prompt
            </button>
            <button
              className={`border-b-2 border-solid ${
                activeTab === 'model' ? 'border-green-100' : 'border-blue-600'
              } pb-1 pl-4 w-full text-left`}
              onClick={() => setActiveTab('model')}
            >
              Model
            </button>
          </div>
          <div className="flex flex-col border-[1px] border-solid border-blue-600 rounded-xl p-2 ml-10">
            <div className="text-2xl text-green-100">23%</div>
            <div className="text-sm text-green-100">accuracy</div>
          </div>
        </div>
        {activeTab === 'evaluate' && (
          <div className="flex flex-col justify-between h-full">
            <div>
              <div className="bg-blue-500 rounded-lg p-4 flex flex-col mb-4">
                Input: The hydraulic pump on the F-16 showed a pressure drop
                during taxi. What are the most likely causes and the next steps
                for inspection?
              </div>
              <div>Rate outputs</div>
              <div className="flex flex-col gap-2 mb-[170px]">
                {tempOutputs.map(output => (
                  <RateOutput output={output.output} tag={output.tag} />
                ))}
              </div>
            </div>
            <div className="mt-4 flex flex-col gap-2">
              <div className="flex flex-wrap">
                <div className="text-sm text-white mb-2 bg-blue-500 rounded-2xl py-2 px-4 w-fit">
                  Whats the most likely fix for Installation of a Fuel Filter
                  happen?
                </div>
                <div className="text-sm text-white mb-2 bg-blue-500 rounded-2xl py-2 px-4 w-fit">
                  whats the most costly software related aircraft error
                </div>
                <div className="text-sm text-white mb-2 bg-blue-500 rounded-2xl py-2 px-4 w-fit">
                  whats the most common error in aircraft maintenance
                </div>
              </div>
              <div className="flex flex-row border-[1px] border-solid border-blue-100 rounded-lg p-2">
                <textarea
                  className="w-full h-18 bg-transparent border-none rounded-lg px-4 py-2 text-lg resize-none focus:outline-none"
                  placeholder="Try another input"
                />
                <button className="bg-blue-100 text-white rounded-lg px-4 py-2 w-fit self-start">
                  Submit
                </button>
              </div>
              <label className="text-sm text-blue-100">
                Not sure where to start? Think about the questions your users
                will actually ask to test model reliability.
              </label>
            </div>
          </div>
        )}
        {activeTab === 'prompt' && <div>Prompt</div>}
        {activeTab === 'model' && <div>Model</div>}
      </div>
    )
  }

  return (
    <div className="h-full w-full flex flex-col gap-2">
      <div>Prompt</div>
      <div className="text-blue-100">
        Test, tune, and train. Add inputs, review outputs, and give feedback to
        shape better prompts and guide the model toward your ideal results.
      </div>
      <div className="bg-blue-500 rounded-lg p-4 flex flex-col">
        <div className="mb-2">Expected outputs</div>
        <div className="text-sm mb-6">
          Help us generate better results, faster
        </div>
        <label className="text-sm mb-2">
          What kind of output are you hoping for?
        </label>
        <textarea
          className="w-full h-18 bg-blue-600 border-none rounded-lg px-4 py-2 text-lg mb-6"
          placeholder="e.g. “Summarize each entry,” “Generate a visual timeline,” “Classify logs,” “Extract sensor anomalies,” “Create a chart,” “Turn this into a checklist,” etc."
        />
        <label className="text-xs text-gray-100 mb-2">Example input</label>
        <input
          className="w-full h-18 bg-blue-600 border-none rounded-lg px-4 py-2 mb-1"
          placeholder="Enter here"
        />
        <label className="text-xs text-blue-100 mb-4">
          Connect your projects to OpenAI
        </label>
        <div className="mb-3">
          What are some expected outputs you'd hope to see?
        </div>
        <label className="text-xs text-gray-100 mb-2">
          Example ideal outputs
        </label>
        <div className="flex flex-col gap-2 mb-6">
          <input
            className="w-full h-18 bg-blue-600 border-none rounded-lg px-4 py-2 "
            placeholder="Enter here"
          />
          <input
            className="w-full h-18 bg-blue-600 border-none rounded-lg px-4 py-2 "
            placeholder="Enter here"
          />
          <input
            className="w-full h-18 bg-blue-600 border-none rounded-lg px-4 py-2 "
            placeholder="Enter here"
          />
        </div>
        <button
          className="bg-blue-200 text-white rounded-lg px-4 py-2 w-fit self-end"
          onClick={() => setHasGeneratedOutputs(true)}
        >
          Generate outputs
        </button>
      </div>
    </div>
  )
}

export default Prompt
