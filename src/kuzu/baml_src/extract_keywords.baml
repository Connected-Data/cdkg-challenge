// Extract the names of tools and technical frameworks mentioned in a talk's transcript
class Entity {
  tag string[] @description("ALWAYS lowercase this value")
  // leave room for other entities to be added in the future
}

// Create a function to extract the resume from a string.
function ExtractTags(text: string) -> Entity {
  client "openai/gpt-4o-mini"
  prompt #"
    Extract techniques/tools/frameworks mentioned in the following text:

    {{ text }}

    {{ ctx.output_format }}

    Return individual names without repetition.
  "#
}

// Test the function with a sample resume. Open the VSCode playground to run this.
test TestOne {
  functions [ExtractTags]
  args {
    text #"
    But at the same time, still be very suitable for for parallelization with things like Dask and
    Ray and RAPIDS and Spark and that. So we've been working on a lot of integration. We pull together
    a lot of packages into this kind of abstraction layer. And I I want to show a few of these here.
    "#
  }
}


test TestTwo {
  functions [ExtractTags]
  args {
    text #"
    However, we've seen that deep learning does a very good job when we don't have to manually compute features.
    So we'll we'll use some of this, some of this insight and have an encoder, that, bypasses this part of, human
    engineering. So this would stick our natural input, to an embedding. And that is great, but that that will
    still not be everything we need to run validation if we didn't have the transition matrix. For that, we can
    use a transition model, to build this local MDP that where we need in order to run value iteration.

    So we see that usually, in in a lot of the cases, the XAV and the ATC do better than the than the PPO
    baseline. And something else that is very interesting to notice is the Excelfin does better than HCC,
    particularly in the first half of the training. So it does well in low data cases, which is one of the main
    things why we're looking at culling in the first place. So this is quite an encouraging result. To draw some
    conclusions, we we looked at we presented this this blueprint, that is applicable if we know a specific algorithm
    will be of interest for solving a natural, a real world task. So we, we see that real world solutions can benefit
    from combining classic algorithms with neural networks, and this is one way of going about it. Then we build on
    the on the findings that graph neural networks are particularly well suited to imitate some algorithms,
    in particular dynamic programming algorithms.
    "#
  }
}
