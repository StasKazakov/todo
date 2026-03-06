import { toast } from "@/components/ui/use-toast";

export const showToast = (title, description, type = "default") => {
  toast({
    title,
    description,
    variant: type, 
  });
};